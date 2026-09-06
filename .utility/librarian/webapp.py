"""The searching surface, for a person.

Obsidian is the *reading* surface and stays it. This is the other half of the
job: finding the handful worth reading out of a hundred and thirty, by narrowing
on what they are rather than by guessing vocabulary.

Shaped like a product catalogue rather than a web search engine, because the
objects are strongly typed — ten closed taxonomy axes plus `permitted_uses` —
and a person narrowing candidates wants to see how those axes fall **across the
set they have**, not a fixed sidebar of every value the vocabulary permits.

## Three surfaces, one engine

This holds **no retrieval logic**. It calls `consult.find_donor` and renders
what comes back: results, facets, components, advisories, coverage. The CLI and
the MCP server call the same functions, so the three cannot disagree about what
the catalogue contains — and that is the single architectural constraint worth
protecting here, because the moment a page starts scoring things itself nobody
can tell which surface is right.

## Deliberately dependency-free and deliberately loopback

Standard library only: no framework, no build step, no CDN. A tool for reading a
local vault should work with the network unplugged, and every asset a page pulls
from elsewhere is a way for it to stop working later. The page is one file.

Binds `127.0.0.1` and refuses anything else, following the same reasoning as the
MCP HTTP transport: a catalogue of one person's research has no business on a
network interface, and refusing is cheaper than explaining the consequences of
allowing.

    python -m librarian web            # http://127.0.0.1:8322
"""
from __future__ import annotations

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from . import consult
from .config import CatalogueConfig, vault_root

DEFAULT_PORT = 8322
LOOPBACK = {"127.0.0.1", "localhost", "::1"}
PAGE = Path(__file__).with_name("webapp.html")


def search(query: str, filters: dict[str, list[str]], limit: int = 25) -> dict[str, Any]:
    """One call into the engine. Everything the page shows comes from here."""
    constraints = {axis: values for axis, values in filters.items()
                   if axis in consult.FILTER_FIELDS and values}
    try:
        response = consult.find_donor(query, constraints, limit)
    except ValueError as exc:
        # An axis value outside its enumeration. The page should say what is
        # permitted rather than render an empty result and imply nothing matched.
        return {"error": str(exc),
                "axes": {a: list(v) for a, v in consult.axis_vocabulary().items()}}
    payload = response.to_dict()
    payload["vault"] = str(vault_root())
    return payload


class Handler(BaseHTTPRequestHandler):
    server_version = "librarian-web"

    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        # Nothing here is meant to be embedded anywhere, and the page loads no
        # third-party asset - so say so rather than relying on it staying true.
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; style-src 'self' 'unsafe-inline'; "
                         "script-src 'self' 'unsafe-inline'; img-src 'self' data:")
        self.end_headers()
        self.wfile.write(body)

    def _guard(self) -> bool:
        """Refuse anything that did not come from this machine.

        `Host` is checked because a browser sends it and a DNS-rebinding attack
        cannot forge it to a loopback name it does not control. Same reasoning
        as the MCP transport's origin allowlist.
        """
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        if host and host not in LOOPBACK:
            self._send(b'{"error":"refused: not a loopback host"}',
                       "application/json", 403)
            return False
        return True

    def do_GET(self) -> None:                          # noqa: N802 - stdlib API
        if not self._guard():
            return
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            try:
                body = PAGE.read_bytes()
            except FileNotFoundError:
                self._send(b"webapp.html is missing beside webapp.py",
                           "text/plain; charset=utf-8", 500)
                return
            self._send(body, "text/html; charset=utf-8")
            return

        if parsed.path == "/api/search":
            params = parse_qs(parsed.query)
            query = (params.get("q") or [""])[0]
            limit = min(100, max(1, int((params.get("limit") or ["25"])[0] or 25)))
            filters = {axis: params[axis] for axis in consult.FILTER_FIELDS
                       if axis in params}
            payload = search(query, filters, limit)
            self._send(json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8",
                       400 if "error" in payload else 200)
            return

        if parsed.path == "/api/axes":
            self._send(json.dumps(
                {a: list(v) for a, v in consult.axis_vocabulary().items()},
                ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8")
            return

        self._send(b'{"error":"no such endpoint"}', "application/json", 404)

    def log_message(self, fmt: str, *args: Any) -> None:
        """Quiet by default. A local tool logging every keystroke to the console
        is noise, and the console is where a real problem needs to be visible."""
        return


def serve(host: str = "127.0.0.1", port: int = DEFAULT_PORT,
          open_browser: bool = True) -> int:
    if host not in LOOPBACK:
        print(f"refused: --host {host} is not a loopback address. This app is "
              f"not built to be reachable from a network.")
        return 2
    httpd = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}/"
    print(f"serving {vault_root()} at {url}")
    print("  Obsidian remains the reading surface; this one is for finding.")
    print("  Ctrl-C to stop.")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
    return 0
