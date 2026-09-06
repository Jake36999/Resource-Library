"""The person surface: what it serves, what it refuses, and what it must not
learn to do itself.

The page is not tested by rendering it — there is no browser here. It is tested
for the three properties that would silently rot: that it stays dependency-free,
that its vocabulary tracks the engine's, and that it holds no retrieval logic.
Each of those is a claim the module docstring makes, and an unenforced claim is
a preference (`FAILURE_MUST_BE_LOUD`).
"""
from __future__ import annotations

import json
import re
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from librarian import consult, webapp


# --------------------------------------------------------------- the endpoint

def test_unknown_axes_are_dropped_rather_than_passed_through(monkeypatch):
    """A query string is user input. Anything not a filter axis is not a
    constraint, and must not reach the engine as one."""
    seen: dict = {}
    monkeypatch.setattr(webapp.consult, "find_donor",
                        lambda q, c, n: seen.update(constraints=c) or _empty())
    webapp.search("anything", {"license_class": ["Permissive"],
                               "drop_table": ["yes"], "ecosystem": []}, 5)
    assert seen["constraints"] == {"license_class": ["Permissive"]}


def test_a_bad_axis_value_returns_the_vocabulary_not_an_empty_result():
    """An empty result and a rejected constraint look identical to a reader.
    The first means nothing matched; the second means nothing was asked."""
    payload = webapp.search("scheduler", {"license_class": ["permissive"]}, 5)
    assert "error" in payload
    assert "Permissive" in payload["axes"]["license_class"]
    assert "results" not in payload


def test_the_payload_names_the_vault_it_answered_from(monkeypatch):
    monkeypatch.setattr(webapp.consult, "find_donor", lambda q, c, n: _empty())
    assert webapp.search("x", {}, 5)["vault"]


# ------------------------------------------------------------------- the wire

@pytest.fixture()
def server(monkeypatch):
    """A real socket on a real ephemeral port, with the engine stubbed out.

    Routing, guards and headers are what is under test; retrieval has its own
    suite and dragging the built index in here would make these tests depend on
    the corpus.
    """
    monkeypatch.setattr(webapp, "search",
                        lambda q, f, n: {"results": [], "query": q,
                                         "filters": f, "limit": n})
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), webapp.Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


def _get(url: str, host: str | None = None):
    request = Request(url)
    if host:
        request.add_header("Host", host)
    with urlopen(request, timeout=5) as response:
        return response.status, response.read()


def test_the_root_serves_the_page(server):
    status, body = _get(server + "/")
    assert status == 200
    assert b"<title>Resource Library</title>" in body


def test_search_forwards_the_query_and_every_repeated_axis(server):
    _, body = _get(server + "/api/search?q=queue&license_class=Permissive"
                            "&license_class=Copyleft&ecosystem=Python&limit=7")
    payload = json.loads(body)
    assert payload["query"] == "queue"
    assert payload["limit"] == 7
    assert payload["filters"] == {"license_class": ["Permissive", "Copyleft"],
                                  "ecosystem": ["Python"]}


def test_limit_is_bounded_rather_than_trusted(server):
    assert json.loads(_get(server + "/api/search?q=a&limit=9999")[1])["limit"] == 100
    assert json.loads(_get(server + "/api/search?q=a&limit=0")[1])["limit"] == 1


def test_axes_serves_the_whole_vocabulary(server):
    axes = json.loads(_get(server + "/api/axes")[1])
    assert set(axes) == set(consult.FILTER_FIELDS)
    assert "Permissive" in axes["license_class"]


def test_a_forged_host_is_refused(server):
    """A page on any site can point a request at 127.0.0.1; what it cannot do is
    forge `Host`. Same reasoning as the MCP transport's origin allowlist."""
    with pytest.raises(HTTPError) as caught:
        _get(server + "/api/search?q=a", host="evil.example.com")
    assert caught.value.code == 403


def test_an_unknown_path_404s_rather_than_serving_the_page(server):
    with pytest.raises(HTTPError) as caught:
        _get(server + "/etc/passwd")
    assert caught.value.code == 404


def test_responses_declare_they_are_not_to_be_embedded(server):
    request = Request(server + "/")
    with urlopen(request, timeout=5) as response:
        assert response.headers["X-Frame-Options"] == "DENY"
        assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_serve_refuses_a_routable_host_before_binding(capsys):
    assert webapp.serve(host="0.0.0.0", port=0, open_browser=False) == 2
    assert "refused" in capsys.readouterr().out


# -------------------------------------------------------------------- the page

@pytest.fixture(scope="module")
def page() -> str:
    return webapp.PAGE.read_text(encoding="utf-8")


def test_the_page_pulls_nothing_from_the_network(page):
    """The claim is that this works with the network unplugged. A CDN link, a
    web font or a remote import would break it silently, months later, offline."""
    remote = re.findall(r'(?:src|href)\s*=\s*"(https?://[^"]+)"', page)
    assert not remote, f"the page would fetch {remote}"
    assert "import(" not in page and "importScripts" not in page


def test_the_page_labels_every_axis_the_engine_can_facet(page):
    """`NO_SCHEMA_DRIFT` across the surface boundary. An axis added to the
    engine and not here renders as a raw column name in the sidebar."""
    block = page.split("const AXIS_LABELS = {")[1].split("};")[0]
    labelled = set(re.findall(r"(\w+):\s*\"", block))
    missing = set(consult.FACET_FIELDS) - labelled
    assert not missing, f"unlabelled axes: {sorted(missing)}"


def test_the_page_never_buries_an_advisory(page):
    """A constraint that removed the best answer, or a question the catalogue
    does not cover, is the most important thing on the screen."""
    assert "p.advisories" in page
    assert "banner" in page
    assert "<details" not in page.split('id="banners"')[0][-400:], \
        "advisories must not be inside a collapsed element"


def test_the_page_holds_no_retrieval_logic(page):
    """Three surfaces, one engine. The moment the page sorts or scores, the CLI
    and the MCP server can disagree with it and nothing says which is right."""
    script = page.split("<script>")[1]
    for forbidden in (".sort(", "bm25", "Math.log", "score *", "* weight"):
        assert forbidden not in script, f"the page is ranking: {forbidden}"


def _empty():
    from librarian.consult import Response

    return Response(intent="donor", results=[], notes=[])
