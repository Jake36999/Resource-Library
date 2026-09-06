"""Embeddings and vector search - step 4, and strictly optional.

Brute-force cosine over float32 vectors in numpy. At the vault's ~1,500 chunks
a full scan is sub-millisecond, so there is no ANN index and there should not
be one until well past a hundred thousand chunks: an index would buy latency
that was never a problem and cost operational burden that is.

Everything here degrades. If LM Studio is not running, or numpy is missing, or
no embeddings have been built, search returns nothing and the caller reports
`partial=True` with a reason. A consult must never fail because an optional
subsystem is down.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import struct
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .config import CatalogueConfig, embedding_base_url

try:                                               # pragma: no cover - env dependent
    import numpy as np
except Exception:                                  # pragma: no cover
    np = None


class EmbeddingsUnavailable(RuntimeError):
    """Raised only by the build path, which has a person watching it.

    The read path never sees this: `search()` returns an empty list instead,
    because a slow or absent embedding server must degrade a query rather
    than break it.
    """


@dataclass(frozen=True)
class EmbedStats:
    embedded: int
    skipped: int
    dims: int
    model: str
    errors: list[str]


def _url(cfg: CatalogueConfig, path: str) -> str:
    base = (embedding_base_url() or cfg.embedding_base_url).rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def list_models(cfg: CatalogueConfig) -> list[str]:
    request = urllib.request.Request(_url(cfg, "/models"), method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8") or "{}")
    return [m.get("id", "") for m in payload.get("data", []) if isinstance(m, dict)]


def resolve_model(cfg: CatalogueConfig, ids: Sequence[str]) -> str | None:
    """Map a configured name onto an id the server will actually accept.

    LM Studio ids carry a quantisation suffix
    (`...nomic-embed-text-v1.5@q4_k_m`). A substring check was enough to say
    "available" and not enough to make the call succeed, which is the worst
    of both: a green status line and an HTTP 400. Resolving to a real id is
    what makes availability mean something.
    """
    if not cfg.embedding_model:
        return next((i for i in ids if "embed" in i.lower()), None)
    if cfg.embedding_model in ids:
        return cfg.embedding_model
    prefixed = [i for i in ids if i.startswith(cfg.embedding_model)]
    if prefixed:
        return sorted(prefixed)[0]
    return None


def available(cfg: CatalogueConfig | None = None) -> tuple[bool, str]:
    """Reachability plus a reason.

    A down server and a running server with no embedding model loaded need
    different responses from the operator, so they get different messages.
    """
    cfg = cfg or CatalogueConfig.load()
    if not cfg.embeddings_enabled:
        return False, "embeddings disabled in library_config.json"
    if np is None:
        return False, "numpy is not installed; vector search is unavailable"
    try:
        ids = list_models(cfg)
    except Exception as exc:
        return False, (
            f"cannot reach LM Studio at {_url(cfg, '')} ({exc}). The desktop app "
            "being open is not sufficient - the local server must be started."
        )
    if not ids:
        return False, "LM Studio is reachable but reports no models."
    resolved = resolve_model(cfg, ids)
    if resolved is None:
        return False, (f"LM Studio is reachable but no model matches "
                       f"'{cfg.embedding_model}' ({len(ids)} other model(s) present).")
    return True, f"embedding model available ({resolved})."


def embed_texts(texts: Sequence[str], cfg: CatalogueConfig | None = None,
                model_id: str | None = None) -> list[list[float]]:
    """One POST per batch to the OpenAI-compatible embeddings route.

    The chat adapter in `.utility/adapters/lmstudio.py` is not reused here
    because it is a chat client - a different route with different failure
    modes - and wrapping it would obscure which of the two is down.
    """
    cfg = cfg or CatalogueConfig.load()
    if not texts:
        return []
    model = model_id or cfg.embedding_model
    body = json.dumps({"model": model, "input": list(texts)}).encode("utf-8")
    request = urllib.request.Request(_url(cfg, "/embeddings"), data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=cfg.embedding_timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:                   # pragma: no cover - network
        try:
            body = exc.read().decode("utf-8")[:300]
        except Exception:
            body = exc.reason
        # The body is the diagnosis. "Bad Request" alone sent this build
        # chasing a model-id bug when the server was actually saying the
        # model had been unloaded mid-queue.
        raise EmbeddingsUnavailable(f"embeddings HTTP {exc.code}: {body}") from exc
    except Exception as exc:                                # pragma: no cover - network
        raise EmbeddingsUnavailable(str(exc)) from exc
    data = sorted(payload.get("data", []), key=lambda item: item.get("index", 0))
    return [list(item.get("embedding", [])) for item in data]


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def pack(vector: Iterable[float]) -> bytes:
    values = list(vector)
    return struct.pack(f"<{len(values)}f", *values)


def unpack(blob: bytes, dims: int) -> list[float]:
    return list(struct.unpack(f"<{dims}f", blob))


def _embed_batch(batch: Sequence[tuple[int, str]], cfg: CatalogueConfig,
                 model: str, attempts: int = 3
                 ) -> tuple[list[list[float]], str]:
    """Embed a batch, retrying, then one text at a time as a last resort.

    `max_task_models_loaded: 1` and a 300s model TTL on this host mean the
    embedding model can be evicted while a batch is queued - the server says
    so plainly ("Model was unloaded while the request was still in queue").
    That is transient, so it is retried; a batch that still fails is split so
    one bad text costs one vector rather than sixteen.
    """
    import time

    texts = [text for _, text in batch]
    last = ""
    for attempt in range(attempts):
        try:
            return embed_texts(texts, cfg, model), ""
        except EmbeddingsUnavailable as exc:
            last = str(exc)
            time.sleep(min(5.0, 1.5 * (attempt + 1)))

    vectors: list[list[float]] = []
    for text in texts:
        try:
            vectors.extend(embed_texts([text], cfg, model))
        except EmbeddingsUnavailable:
            vectors.append([])
    if any(vectors):
        return vectors, f"{last} (recovered by embedding one at a time)"
    return [], last


# --------------------------------------------------------------------- build

def build(db_path: Path | None = None, cfg: CatalogueConfig | None = None, *,
          rebuild: bool = False, batch_size: int | None = None) -> EmbedStats:
    """Embed every chunk that does not already have a current vector.

    Chunks are keyed by a hash of their text, so re-running after an index
    build only pays for what actually changed.
    """
    from . import index as index_mod

    cfg = cfg or CatalogueConfig.load()
    ok, reason = available(cfg)
    if not ok:
        raise EmbeddingsUnavailable(reason)
    model = resolve_model(cfg, list_models(cfg)) or cfg.embedding_model

    size = batch_size or cfg.embedding_batch_size
    errors: list[str] = []
    embedded = skipped = 0
    dims = 0

    conn = index_mod.connect(db_path)
    try:
        index_mod.init(conn)
        if rebuild:
            conn.execute("DELETE FROM embedding")
        rows = conn.execute(
            "SELECT c.id AS id, c.text AS text, c.heading AS heading, c.note AS note, "
            "       e.text_hash AS existing, e.model AS model "
            "FROM chunk c LEFT JOIN embedding e ON e.chunk_id = c.id "
            "ORDER BY c.id").fetchall()

        pending: list[tuple[int, str]] = []
        for row in rows:
            # Heading and note name go into the embedded text: `## Bottom Line`
            # of note X means something the bare paragraph does not.
            text = f"{row['note']} :: {row['heading'] or ''}\n{row['text']}".strip()
            digest = text_hash(text)
            if row["existing"] == digest and row["model"] == model:
                skipped += 1
                continue
            pending.append((row["id"], text))

        for start in range(0, len(pending), size):
            batch = pending[start:start + size]
            vectors, failure = _embed_batch(batch, cfg, model)
            if failure:
                errors.append(f"batch at {start}: {failure}")
                if not vectors:
                    break
            for (chunk_id, text), vector in zip(batch, vectors):
                if not vector:
                    errors.append(f"chunk {chunk_id}: empty vector")
                    continue
                dims = len(vector)
                try:
                    conn.execute(
                        "INSERT OR REPLACE INTO embedding(chunk_id, model, vector, "
                        "dims, text_hash) VALUES(?,?,?,?,?)",
                        (chunk_id, model, pack(vector), dims, text_hash(text)))
                except sqlite3.IntegrityError:
                    # The chunk went away while this run was in flight - an
                    # index build reindexed its note. Losing one vector is the
                    # right cost; losing the whole run to it is not.
                    skipped += 1
                    errors.append(f"chunk {chunk_id} disappeared mid-run "
                                  f"(concurrent index build); skipped")
                    continue
                embedded += 1
            conn.commit()

        index_mod.stamp(conn, "embeddings_model", model)
        index_mod.stamp(conn, "embeddings_built_at", index_mod.now_iso())
        conn.commit()
    finally:
        conn.close()
    return EmbedStats(embedded=embedded, skipped=skipped, dims=dims,
                      model=model, errors=errors)


# -------------------------------------------------------------------- search

def search(conn: sqlite3.Connection, query: str, cfg: CatalogueConfig | None = None,
           limit: int = 50, layers: Sequence[str] | None = None
           ) -> tuple[list[tuple[int, str, float]], str]:
    """Return (hits, note). Hits are `(chunk_id, note_name, cosine)`.

    Never raises. The second element explains an empty result - "no
    embeddings built", "LM Studio unreachable" - so `Response.notes` can
    tell the caller what was missing rather than silently returning less.
    """
    cfg = cfg or CatalogueConfig.load()
    if np is None:
        return [], "numpy is not installed; vector search skipped"
    row = conn.execute("SELECT COUNT(*) AS n FROM embedding").fetchone()
    if not row or not row["n"]:
        return [], "no embeddings built; run `python -m librarian embed`"

    stored = conn.execute("SELECT model FROM embedding LIMIT 1").fetchone()
    try:
        vectors = embed_texts([query], cfg, stored["model"] if stored else None)
    except EmbeddingsUnavailable as exc:
        return [], f"vector search skipped: {exc}"
    if not vectors or not vectors[0]:
        return [], "vector search skipped: embedding server returned nothing"

    sql = ("SELECT e.chunk_id AS chunk_id, e.vector AS vector, e.dims AS dims, "
           "c.note AS note FROM embedding e JOIN chunk c ON c.id = e.chunk_id")
    params: list[object] = []
    if layers:
        marks = ",".join("?" for _ in layers)
        sql += f" WHERE c.layer IN ({marks})"
        params.extend(layers)
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        return [], "no embeddings for the requested layers"

    dims = rows[0]["dims"]
    matrix = np.frombuffer(b"".join(r["vector"] for r in rows if r["dims"] == dims),
                           dtype="<f4").reshape(-1, dims)
    usable = [r for r in rows if r["dims"] == dims]
    query_vec = np.asarray(vectors[0][:dims], dtype="<f4")

    norms = np.linalg.norm(matrix, axis=1)
    query_norm = float(np.linalg.norm(query_vec)) or 1.0
    scores = (matrix @ query_vec) / (np.where(norms == 0, 1.0, norms) * query_norm)

    order = np.argsort(-scores)[:limit]
    hits = [(usable[i]["chunk_id"], usable[i]["note"], float(scores[i])) for i in order]
    return hits, ""
