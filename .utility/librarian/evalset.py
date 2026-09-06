"""The retrieval evaluation set.

Twenty questions with known-correct answers. Without this you cannot tell
whether a retrieval change helped, which makes every later tuning decision a
matter of taste - so it is built alongside the filter-only implementation
rather than after the embeddings, and the number it prints before embeddings
exist is the baseline the embeddings have to beat.

Two numbers are reported and they answer different questions:

    hit@k     did the right answer appear at all
    recall@k  what fraction of the expected answers appeared

`hit@k` is the one the acceptance criterion names, because a question with a
single correct answer is the common case here.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from . import consult
from .config import CatalogueConfig, EVAL_PATH


@dataclass(frozen=True)
class Question:
    id: str
    question: str
    intent: str
    expects: tuple[str, ...]
    filters: dict[str, Any] | None = None
    source: str | None = None
    why: str = ""


@dataclass(frozen=True)
class QuestionResult:
    question: Question
    returned: tuple[str, ...]
    found: tuple[str, ...]
    best_rank: int | None       # 1-based position of the first expected answer

    @property
    def hit(self) -> bool:
        return bool(self.found)

    @property
    def recall(self) -> float:
        return len(self.found) / len(self.question.expects) if self.question.expects else 0.0


@dataclass(frozen=True)
class EvalReport:
    k: int
    results: tuple[QuestionResult, ...]
    partial_queries: int
    notes: tuple[str, ...]

    @property
    def hit_rate(self) -> float:
        return (sum(1 for r in self.results if r.hit) / len(self.results)
                if self.results else 0.0)

    @property
    def recall_at_k(self) -> float:
        return (sum(r.recall for r in self.results) / len(self.results)
                if self.results else 0.0)

    @property
    def mean_reciprocal_rank(self) -> float:
        total = sum(1.0 / r.best_rank for r in self.results if r.best_rank)
        return total / len(self.results) if self.results else 0.0


def load(path: Path | None = None) -> tuple[list[Question], int]:
    doc = json.loads(Path(path or EVAL_PATH).read_text(encoding="utf-8"))
    questions = [
        Question(id=item["id"], question=item["question"], intent=item["intent"],
                 expects=tuple(item.get("expects", [])),
                 filters=item.get("filters"), source=item.get("source"),
                 why=item.get("why", ""))
        for item in doc["questions"]
    ]
    return questions, int(doc.get("k", 5))


def ask(question: Question, k: int, *, db_path: Path | None = None,
        cfg: CatalogueConfig | None = None) -> consult.Response:
    limit = max(k, 5)
    if question.intent == "orient":
        return consult.orient(question.question, limit, db_path=db_path, cfg=cfg)
    if question.intent == "donor":
        return consult.find_donor(question.question, question.filters, limit,
                                  db_path=db_path, cfg=cfg)
    if question.intent == "pattern":
        return consult.find_pattern(question.question, limit, db_path=db_path, cfg=cfg)
    if question.intent == "technique":
        return consult.find_technique(question.question, question.source, limit,
                                      db_path=db_path, cfg=cfg)
    if question.intent == "data":
        return consult.find_data(question.question, None, limit, db_path=db_path, cfg=cfg)
    return consult.find_precedent(question.question, limit, db_path=db_path, cfg=cfg)


def run(path: Path | None = None, *, db_path: Path | None = None,
        cfg: CatalogueConfig | None = None, k: int | None = None) -> EvalReport:
    questions, default_k = load(path)
    top = k or default_k
    results: list[QuestionResult] = []
    partial = 0
    notes: set[str] = set()

    for question in questions:
        response = ask(question, top, db_path=db_path, cfg=cfg)
        if response.partial:
            partial += 1
            notes.update(response.notes)
        returned = tuple(r.name for r in response.results[:top])
        found = tuple(e for e in question.expects if e in returned)
        best = next((i for i, name in enumerate(returned, start=1)
                     if name in question.expects), None)
        results.append(QuestionResult(question, returned, found, best))

    return EvalReport(k=top, results=tuple(results), partial_queries=partial,
                      notes=tuple(sorted(notes)))


def format_report(report: EvalReport) -> str:
    lines = [f"Retrieval evaluation - {len(report.results)} questions, k={report.k}", ""]
    for result in report.results:
        mark = "hit " if result.hit else "MISS"
        position = f"@{result.best_rank}" if result.best_rank else "  "
        lines.append(f"  {mark} {position:3}  {result.question.id:28} "
                     f"{result.question.intent:9} expects {list(result.question.expects)}")
        if not result.hit:
            lines.append(f"        returned: {list(result.returned)}")
    lines.append("")
    lines.append(f"  hit@{report.k}     {report.hit_rate:.2f}   "
                 f"({sum(1 for r in report.results if r.hit)}/{len(report.results)})")
    lines.append(f"  recall@{report.k}  {report.recall_at_k:.2f}")
    lines.append(f"  MRR        {report.mean_reciprocal_rank:.2f}")
    if report.partial_queries:
        lines.append(f"  {report.partial_queries} queries ran partial:")
        for note in report.notes:
            lines.append(f"    - {note}")
    return "\n".join(lines)
