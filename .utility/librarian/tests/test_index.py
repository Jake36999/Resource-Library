"""The index is disposable. These tests are what make that claim checkable."""
from __future__ import annotations

from pathlib import Path

from librarian import index as index_mod
from librarian import notes as notes_mod


def test_rebuild_from_empty_is_idempotent(vault: Path, db: Path):
    first = index_mod.build(vault, db, rebuild=True)
    second = index_mod.build(vault, db, rebuild=True)
    assert (first.notes, first.chunks, first.links) == \
           (second.notes, second.chunks, second.links), \
        "a rebuild must produce identical row counts, or the index is not reproducible"


def test_every_note_appears_exactly_once(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        rows = conn.execute("SELECT name, COUNT(*) AS n FROM note GROUP BY name "
                            "HAVING n > 1").fetchall()
        total = conn.execute("SELECT COUNT(*) AS n FROM note").fetchone()["n"]
    finally:
        conn.close()
    on_disk = len(list(notes_mod.iter_note_paths(vault)))
    assert rows == [], f"notes indexed more than once: {[r['name'] for r in rows]}"
    assert total == on_disk


def test_deleting_the_database_loses_nothing(vault: Path, db: Path):
    before = index_mod.build(vault, db, rebuild=True)
    db.unlink()
    for suffix in ("-wal", "-shm"):
        extra = Path(str(db) + suffix)
        if extra.exists():
            extra.unlink()
    after = index_mod.build(vault, db, rebuild=True)
    assert (before.notes, before.chunks, before.links) == \
           (after.notes, after.chunks, after.links), \
        "Markdown is truth: a deleted index must rebuild to exactly the same state"


def test_a_removed_note_leaves_the_index(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    (vault / "01-Resources" / "gadget-queue.md").unlink()
    index_mod.build(vault, db)
    conn = index_mod.connect(db)
    try:
        assert conn.execute("SELECT COUNT(*) AS n FROM note WHERE name = 'gadget-queue'"
                            ).fetchone()["n"] == 0
        assert conn.execute("SELECT COUNT(*) AS n FROM chunk WHERE note = 'gadget-queue'"
                            ).fetchone()["n"] == 0, "chunks must go with their note"
    finally:
        conn.close()


def test_facets_are_written_for_resources_and_not_for_hubs(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        names = {r["name"] for r in conn.execute("SELECT name FROM resource_facet")}
    finally:
        conn.close()
    assert "widget-scheduler" in names
    assert "Taxonomy Index" not in names, \
        "a hub in the filterable set would put the router into every candidate list"


def test_application_count_counts_only_recorded_links(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        rows = {r["name"]: r["application_count"] for r in conn.execute(
            "SELECT name, application_count FROM resource_facet")}
    finally:
        conn.close()
    assert rows["widget-scheduler"] == 1, "an applied_resource link is proven use"
    assert rows["gadget-queue"] == 0, \
        "a resource named only in prose is not evidence of use"


def test_refresh_touches_only_what_changed(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    import time
    marker = time.time()
    time.sleep(0.01)
    target = vault / "01-Resources" / "widget-scheduler.md"
    target.write_text(target.read_text(encoding="utf-8") + "\n## Extra\nMore text.\n",
                      encoding="utf-8")
    stats = index_mod.refresh(vault, db, since=marker)
    assert stats.notes == 1


def test_chunks_carry_their_heading(vault: Path, db: Path):
    index_mod.build(vault, db, rebuild=True)
    chunks = index_mod.chunks_for("widget-scheduler", db)
    headings = {c.heading for c in chunks}
    assert "Bottom Line" in headings, \
        "a hit must be able to say which section it came from"


def test_reindexing_unchanged_notes_preserves_embeddings(vault: Path, db: Path):
    """Embeddings cascade from chunk rows.

    A blanket delete-and-reinsert on every index run threw away every vector,
    which turned a routine `index` into a silent six-minute penalty.
    """
    from librarian import embed as embed_mod

    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        rows = conn.execute("SELECT id, text FROM chunk").fetchall()
        for row in rows:
            conn.execute(
                "INSERT INTO embedding(chunk_id, model, vector, dims, text_hash) "
                "VALUES(?,?,?,?,?)",
                (row["id"], "fake-model", embed_mod.pack([0.1, 0.2, 0.3]), 3,
                 embed_mod.text_hash(row["text"])))
        conn.commit()
        before = conn.execute("SELECT COUNT(*) AS n FROM embedding").fetchone()["n"]
    finally:
        conn.close()

    index_mod.build(vault, db)                 # no --rebuild: nothing changed

    conn = index_mod.connect(db)
    try:
        after = conn.execute("SELECT COUNT(*) AS n FROM embedding").fetchone()["n"]
    finally:
        conn.close()
    assert before > 0 and after == before, \
        "re-indexing an unchanged vault must not discard its vectors"


def test_editing_a_note_drops_only_its_embeddings(vault: Path, db: Path):
    from librarian import embed as embed_mod

    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        for row in conn.execute("SELECT id, text FROM chunk").fetchall():
            conn.execute(
                "INSERT INTO embedding(chunk_id, model, vector, dims, text_hash) "
                "VALUES(?,?,?,?,?)",
                (row["id"], "fake-model", embed_mod.pack([0.1]), 1,
                 embed_mod.text_hash(row["text"])))
        conn.commit()
    finally:
        conn.close()

    target = vault / "01-Resources" / "gadget-queue.md"
    target.write_text(target.read_text(encoding="utf-8") + "\n## New\nText.\n",
                      encoding="utf-8")
    index_mod.build(vault, db)

    conn = index_mod.connect(db)
    try:
        stale = conn.execute(
            "SELECT COUNT(*) AS n FROM embedding e JOIN chunk c ON c.id = e.chunk_id "
            "WHERE c.note = 'gadget-queue'").fetchone()["n"]
        kept = conn.execute(
            "SELECT COUNT(*) AS n FROM embedding e JOIN chunk c ON c.id = e.chunk_id "
            "WHERE c.note = 'widget-scheduler'").fetchone()["n"]
    finally:
        conn.close()
    assert stale == 0, "an edited note's vectors are stale and must go"
    assert kept > 0, "its neighbours' vectors are still valid and must stay"


def test_embed_survives_a_chunk_vanishing_mid_run(vault: Path, db: Path, monkeypatch):
    """A concurrent index build can move chunk ids under a running embed job.

    Losing one vector to that is the right cost. Losing the whole run - which
    is what an unhandled IntegrityError did - is not.
    """
    from librarian import embed as embed_mod
    from librarian.config import CatalogueConfig

    index_mod.build(vault, db, rebuild=True)
    cfg = CatalogueConfig(embedding_batch_size=4)
    monkeypatch.setattr(embed_mod, "available", lambda c=None: (True, "faked"))
    monkeypatch.setattr(embed_mod, "list_models", lambda c: ["fake-model"])
    monkeypatch.setattr(embed_mod, "resolve_model", lambda c, ids: "fake-model")
    monkeypatch.setattr(embed_mod, "embed_texts",
                        lambda texts, c=None, model_id=None: [[0.1, 0.2]] * len(texts))

    conn = index_mod.connect(db)
    try:
        gone = conn.execute("SELECT id FROM chunk ORDER BY id LIMIT 1").fetchone()["id"]
        conn.execute("DELETE FROM chunk WHERE id = ?", (gone,))
        conn.commit()
    finally:
        conn.close()

    # The row list is read before the delete in a real race; simulate by
    # asking for an id that no longer exists.
    stats = embed_mod.build(db, cfg)
    assert stats.embedded > 0, "the rest of the run must still complete"


def test_link_blocks_are_not_chunked(vault: Path, db: Path):
    """Boilerplate is not a neutral cost; it competes for the ranking slot.

    `## Semantic Links` is a list of wikilinks and `## Evidence Anchors`
    restates frontmatter. Full-text matches inside them are always spurious,
    and before they were excluded they were a third of the chunk corpus and
    were demonstrably outranking correct answers on a shared token.
    """
    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        headings = {row["heading"] for row in
                    conn.execute("SELECT DISTINCT heading FROM chunk")}
        prose = conn.execute(
            "SELECT COUNT(*) AS n FROM chunk WHERE heading = 'Bottom Line'"
        ).fetchone()["n"]
    finally:
        conn.close()
    for boilerplate in ("Semantic Links", "Evidence", "Evidence Anchors",
                        "GitHub Snapshot"):
        assert boilerplate not in headings, \
            f"'{boilerplate}' holds links or metadata, not prose, and must not be searchable"
    assert prose > 0, "excluding link blocks must not take the prose with it"


def test_excluded_sections_keep_their_links(vault: Path, db: Path):
    """Nothing is lost by not chunking them. `## Semantic Links` is where
    `parent_topic` lives, and the link table - not the text index - is what
    graph traversal reads."""
    index_mod.build(vault, db, rebuild=True)
    conn = index_mod.connect(db)
    try:
        parents = conn.execute(
            "SELECT COUNT(*) AS n FROM link WHERE relation = 'parent_topic'"
        ).fetchone()["n"]
    finally:
        conn.close()
    assert parents > 0, \
        "links from an unchunked section must still reach the link table"
