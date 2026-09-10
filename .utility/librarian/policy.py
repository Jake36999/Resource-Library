"""Policy as code, with named codes.

Following `local_tool_assist_mcp/policy.py`: a refusal names the rule that
refused and says why, because a generic error tells the caller nothing about
what to do differently. Every code below appears in section 2 of the Design
Specification; nothing refuses without a code.

The action registry is a frozenset derived from the registered entries. That
is the whole of the extension policy's enforcement: an agent that needs a
capability the registry lacks is blocked, and being blocked is the intended
outcome - it produces a decision point rather than a one-off script.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyError(Exception):
    """A refusal that can explain itself."""

    code: str
    message: str
    blocked: bool = True

    def __str__(self) -> str:                      # pragma: no cover - trivial
        return f"{self.code}: {self.message}"

    def to_result(self) -> dict:
        return {"status": "blocked" if self.blocked else "refused",
                "code": self.code, "message": self.message}


# --------------------------------------------------------------- structural

READ_ONLY_CONSULT = "READ_ONLY_CONSULT"
EXECUTION_SANDBOX_ONLY = "EXECUTION_SANDBOX_ONLY"
DOCUMENT_BEFORE_DESTROY = "DOCUMENT_BEFORE_DESTROY"
CLOSED_ACTION_REGISTRY = "CLOSED_ACTION_REGISTRY"
NO_ARBITRARY_SHELL = "NO_ARBITRARY_SHELL"
NO_SCHEMA_DRIFT = "NO_SCHEMA_DRIFT"
MARKDOWN_IS_TRUTH = "MARKDOWN_IS_TRUTH"
EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"
NO_PERSISTENT_SOURCE_GRAPH = "NO_PERSISTENT_SOURCE_GRAPH"
GRAPH_IS_DERIVED = "GRAPH_IS_DERIVED"
GRAPH_ADVISORY_ONLY = "GRAPH_ADVISORY_ONLY"
CENTRALITY_MUST_BE_FILTERED = "CENTRALITY_MUST_BE_FILTERED"

# --------------------------------------------------------------- intake gates

MANIFEST_REQUIRED = "MANIFEST_REQUIRED"
DOCTOR_PASS_WARN_REQUIRED = "DOCTOR_PASS_WARN_REQUIRED"
REVIEW_APPROVAL_REQUIRED = "REVIEW_APPROVAL_REQUIRED"
COHORT_FROZEN_REQUIRED = "COHORT_FROZEN_REQUIRED"
SENSITIVITY_REVIEW = "SENSITIVITY_REVIEW"

# --------------------------------------------------- contribution (stage 5)
#
# An outside agent may add to the catalogue. These are the four rules that make
# that safe, and each one refuses by name rather than by silence.

STAGING_BEFORE_VAULT = "STAGING_BEFORE_VAULT"
# A scouting prompt may look at anything; a scouting reply may only take a
# shape the caller declared. Open question, closed answer.
OPEN_ANALYSIS_STRICT_RETURN = "OPEN_ANALYSIS_STRICT_RETURN"
BRIEF_REQUIRED = "BRIEF_REQUIRED"
DISPOSITION_REQUIRED = "DISPOSITION_REQUIRED"
INTERPRETATION_IS_NOT_MACHINE_WORK = "INTERPRETATION_IS_NOT_MACHINE_WORK"

# The only write Mode C may perform. Anything else touching the vault from a
# read path is a defect, not a special case.
CONSULT_WRITE_ALLOWED = frozenset({"record_application"})

# The closed action registry. Membership is the whole permission model, and
# the set is frozen at import so nothing can widen it at runtime.
REGISTERED_ACTIONS = frozenset({
    # read surface
    "orient", "find_donor", "find_pattern", "find_technique", "find_data",
    "find_precedent", "get_note", "record_application",
    # index and integrity
    "index_build", "index_refresh", "integrity_run", "embed_build",
    "graph_build",
    # intake, delegated to the ToolSet
    "scan_directory", "validate_manifest", "run_semantic_slice",
    "investigate_repository", "git_shallow_clone", "discard_clone",
    # graphify is a subprocess and is not exempt from NO_ARBITRARY_SHELL
    # because it happens to be useful (spec 4B.3 R5).
    "graphify_build", "graphify_query",
    # workbench, Mode D only
    "workbench_open", "workbench_document", "workbench_close",
    "access_point_verify",
    # contribution: briefs and staged proposals. None of these reaches
    # `01-Resources/` except `promote_proposal`, which is its own tier.
    "open_brief", "list_briefs", "claim_brief", "close_brief",
    "propose_resource", "list_proposals", "promote_proposal",
    # the other direction: something already in use that is not catalogued
    "log_use", "list_queue",
})

# Writes that never touch the vault. An agent holding only these can fill the
# staging area all day and cannot change a single note a reader will see.
STAGING_ONLY_ACTIONS = frozenset({
    "open_brief", "claim_brief", "close_brief",
    "propose_resource", "log_use",
})

# Actions a sweep (Mode A) may never reach. Unattended execution of
# unreviewed code is the one thing this design exists to prevent.
SWEEP_FORBIDDEN_ACTIONS = frozenset({
    "workbench_open", "workbench_document", "workbench_close",
})


def check_action(name: str) -> None:
    """Raise unless `name` is registered. An unregistered name is an error,
    never an improvisation."""
    if name not in REGISTERED_ACTIONS:
        raise PolicyError(
            CLOSED_ACTION_REGISTRY,
            f"'{name}' is not a registered action. Registry changes require the "
            f"user; report the gap rather than working around it.",
        )


def check_sweep_action(name: str) -> None:
    """Raise if a sweep is reaching for something only a person may do."""
    check_action(name)
    if name in SWEEP_FORBIDDEN_ACTIONS:
        raise PolicyError(
            EXECUTION_SANDBOX_ONLY,
            f"'{name}' is Mode D only. A sweep is unattended, and unattended "
            f"execution of unreviewed code is forbidden.",
        )


def check_consult_write(name: str) -> None:
    """Mode C may write exactly one thing."""
    if name not in CONSULT_WRITE_ALLOWED:
        raise PolicyError(
            READ_ONLY_CONSULT,
            f"the consult surface may not write '{name}'. The single permitted "
            f"write is record_application.",
        )


def check_evidence(field: str, value: object, source: str | None) -> None:
    """No factual field is written without a fetched source.

    "Unknown" is a valid value; a plausible guess is not - which is why an
    explicit unknown passes and an unsourced assertion does not.
    """
    if value in (None, "", "Unknown", "unknown"):
        return
    if not source:
        raise PolicyError(
            EVIDENCE_REQUIRED,
            f"'{field}' was given a value with no fetched source. Write "
            f"\"Unknown\" instead of a plausible guess.",
        )


def check_no_schema_drift(known_fields: set[str], incoming: set[str]) -> None:
    """Note schema changes only by editing the authoritative Markdown."""
    added = incoming - known_fields
    if added:
        raise PolicyError(
            NO_SCHEMA_DRIFT,
            "no process may add a note field. New fields must be introduced by "
            f"editing the schema note first: {sorted(added)}",
        )
