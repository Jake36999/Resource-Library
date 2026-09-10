"""Fetching text from the open web, politely, without an API quota.

## Two jobs

**Getting README text without spending GitHub's 60-an-hour budget.** The API
route costs one call per repository, which halves how many can be charted in a
window. `raw.githubusercontent.com` serves the same bytes and is not part of
that budget, so it is tried first and the API stays the fallback.

**Reading sources that are not repositories at all.** A catalogue restricted to
GitHub is restricted to a fraction of what is worth recording — course
material, standards documents, papers, tool documentation. This is the part
that lets those in.

## Politeness is not optional and is not decoration

An unattended overnight job hitting arbitrary hosts is a crawler, and a crawler
that ignores `robots.txt` or hammers a host is one somebody blocks. So:

- `robots.txt` is fetched once per host, cached, and honoured. A disallowed
  path returns nothing and says why — it does not fetch anyway and hope.
- One request per host at a time, with a minimum interval between them.
- A real User-Agent naming the tool, so an operator who wants to complain can.
- A size cap, because a research tool has no business downloading an ISO.

None of that is enforced by the network; it is enforced here or not at all.

## What comes back

Text, and a record of where it came from. HTML is reduced with the standard
library's own parser — no dependency, and `<script>`, `<style>` and `<nav>`
are dropped rather than flattened into the prose, because a page's navigation
is not what the page says.
"""
from __future__ import annotations

import gzip
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any

USER_AGENT = ("librarian/1.0 (+resource-library; personal research catalogue; "
              "contact via repository owner)")

MAX_BYTES = 4_000_000
TIMEOUT = 30
MIN_INTERVAL = 1.0            # seconds between requests to one host

# Tags whose text is not the document's text.
DROP = {"script", "style", "noscript", "nav", "header", "footer", "svg",
        "form", "button", "aside", "template", "iframe"}
BREAK = {"p", "div", "br", "li", "tr", "section", "article",
         "h1", "h2", "h3", "h4", "h5", "h6", "pre", "blockquote"}

RAW_HOST = "https://raw.githubusercontent.com"
README_NAMES = ("README.md", "readme.md", "README.rst", "README.txt",
                "README", "docs/README.md")


class FetchRefused(RuntimeError):
    """Refused before the request was made. Names the rule, like every other
    refusal in this system."""


@dataclass
class Page:
    url: str
    text: str = ""
    content_type: str = ""
    status: int = 0
    fetched_at: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.text) and not self.error


@dataclass
class Fetcher:
    """Holds the politeness state. One per run, not one per call."""

    user_agent: str = USER_AGENT
    min_interval: float = MIN_INTERVAL
    timeout: int = TIMEOUT
    max_bytes: int = MAX_BYTES
    obey_robots: bool = True
    _last: dict[str, float] = field(default_factory=dict, repr=False)
    _robots: dict[str, Any] = field(default_factory=dict, repr=False)

    # -- politeness --------------------------------------------------------

    def _wait(self, host: str) -> None:
        last = self._last.get(host)
        if last is not None:
            gap = self.min_interval - (time.monotonic() - last)
            if gap > 0:
                time.sleep(gap)
        self._last[host] = time.monotonic()

    def allowed(self, url: str) -> tuple[bool, str]:
        """`robots.txt`, fetched once per host and cached.

        A host with no `robots.txt`, or one that cannot be parsed, is treated
        as permitting - that is what the standard says and what every other
        client does. A host that says no means no.
        """
        if not self.obey_robots:
            return True, ""
        parts = urllib.parse.urlsplit(url)
        host = f"{parts.scheme}://{parts.netloc}"
        if host not in self._robots:
            self._robots[host] = self._read_robots(host, parts.netloc)
        parser = self._robots[host]
        if parser is None:
            return True, ""
        if parser.can_fetch(self.user_agent, url):
            return True, ""
        return False, f"{host}/robots.txt disallows this path for our agent"

    def _read_robots(self, host: str, netloc: str):
        """Fetch `robots.txt` with *our* user agent, then parse it.

        `RobotFileParser.read()` cannot be used directly: it fetches with
        urllib's default `Python-urllib/3.x`, which a great many hosts answer
        with 403 - and the parser reads a 403 as *disallow everything*. That
        turned a site whose robots.txt disallows only `/admin` into a site we
        refused entirely, and it would have done the same to most of the web.

        A genuine 401 or 403, seen while presenting a real agent, still means
        disallow-all as the standard says.
        """
        parser = urllib.robotparser.RobotFileParser()
        parser.set_url(f"{host}/robots.txt")
        request = urllib.request.Request(f"{host}/robots.txt", method="GET")
        request.add_header("User-Agent", self.user_agent)
        try:
            self._wait(netloc)
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(200_000).decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                parser.disallow_all = True
                return parser
            return None                                      # 404 and friends: permit
        except Exception:                                    # noqa: BLE001
            return None                                      # unreachable: permit
        parser.parse(body.splitlines())
        return parser

    # -- the fetch ---------------------------------------------------------

    def get(self, url: str) -> Page:
        """One request. Never raises for a network problem; returns the reason.

        An unattended run over forty hosts will meet a dead one, and stopping
        the run for it would be the wrong trade.
        """
        page = Page(url=url)
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("http", "https"):
            page.error = f"refused: {parts.scheme or 'no'} scheme is not fetchable"
            return page

        permitted, reason = self.allowed(url)
        if not permitted:
            page.error = f"refused: {reason}"
            return page

        self._wait(parts.netloc)
        request = urllib.request.Request(url, method="GET")
        request.add_header("User-Agent", self.user_agent)
        request.add_header("Accept", "text/html,text/plain,text/markdown,*/*")
        request.add_header("Accept-Encoding", "gzip")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                page.status = response.status
                page.content_type = (response.headers.get("Content-Type") or "").lower()
                raw = response.read(self.max_bytes + 1)
                if response.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
        except urllib.error.HTTPError as exc:
            page.status = exc.code
            page.error = f"http {exc.code}"
            return page
        except Exception as exc:                            # noqa: BLE001
            page.error = f"{type(exc).__name__}: {exc}"
            return page

        if len(raw) > self.max_bytes:
            page.error = f"refused: larger than {self.max_bytes} bytes"
            return page

        body = raw.decode("utf-8", errors="replace")
        page.text = to_text(body) if _is_html(page.content_type, body) else body
        page.fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return page

    # -- the GitHub shortcut ----------------------------------------------

    def readme(self, repo_key: str, branches: tuple[str, ...] = ("HEAD",)) -> Page:
        """A repository's README without spending API budget.

        `raw.githubusercontent.com` serves the same bytes as the API's readme
        endpoint and is not counted against the 60-an-hour limit, which is the
        difference between charting twenty-eight repositories in a window and
        charting fifty-six.
        """
        last = Page(url="", error="no README found")
        for branch in branches:
            for name in README_NAMES:
                page = self.get(f"{RAW_HOST}/{repo_key}/{branch}/{name}")
                if page.ok:
                    return page
                if page.status not in (404, 0):
                    last = page
        return last


# ---------------------------------------------------------------- HTML

def _is_html(content_type: str, body: str) -> bool:
    if "html" in content_type:
        return True
    if content_type:
        return False
    return bool(re.search(r"<\s*(html|body|div|p)\b", body[:2000], re.I))


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in DROP:
            self.skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag in BREAK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in DROP and self.skip:
            self.skip -= 1
        elif tag == "title":
            self._in_title = False
        elif tag in BREAK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip and data.strip():
            self.parts.append(data)


def to_text(html: str) -> str:
    """HTML to readable text, with the furniture removed.

    Deliberately not a readability implementation. It drops the tags whose
    contents are never the document, collapses whitespace, and stops - which is
    enough for a model to describe a page and is one file with no dependency.
    """
    parser = _Text()
    try:
        parser.feed(html)
    except Exception:                                       # noqa: BLE001
        return re.sub(r"<[^>]+>", " ", html)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    body = "\n".join(line for line in lines if line)
    return (f"# {parser.title.strip()}\n\n{body}" if parser.title.strip()
            else body)
