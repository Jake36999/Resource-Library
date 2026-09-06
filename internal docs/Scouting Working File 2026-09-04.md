---
type: "working_file"
status: "active"
created: "2026-09-04"
cohort: "2026-09-04"
sources_charted: 49
purpose: "how the second cohort was read, and the limit on what any of it may be taken to assert"
---

# Scouting Working File 2026-09-04

## What This Records

Forty-nine sources were charted on 2026-09-04, completing the *Potentially high return*
section of [[repositories to chart]]. This note records the method and, more importantly,
**the ceiling on what the resulting notes are entitled to claim**. The per-note
`## Evidence` blocks state depth of read individually; this states the thing that is true
of all of them at once and would otherwise have to be inferred from forty-nine repetitions.

## The Method

1. **Locate and verify.** One GitHub REST call per repository against the unauthenticated
   60/hour limit, with the run sleeping through resets and resumable from disk. All 49
   resolved; none was renamed, missing or a redirect.
2. **Survey.** A depth-1 blobless clone (`--filter=blob:none --no-checkout`) per repository,
   then `git ls-tree -r HEAD`. This runs over the git protocol and costs no REST quota,
   which is why 49 complete file trees were affordable where 49 API tree calls were not.
   The survey records top-level and second-level directory counts, file extensions, root
   files, and thirteen categorised signals — tests, fixtures, schemas, grammars, notebooks,
   benchmarks, containers, agent instructions, infrastructure and more.
3. **Resolve licences.** Seventeen repositories returned `NOASSERTION` or nothing from the
   API. Their LICENSE variants and READMEs were fetched raw and classified by
   `scout.rank.license_from_text`. Results in [[Licence Resolution 2026-09-03]].
4. **Classify and write.** Against the closed axes in [[Note Content Model]] and the domain
   boundaries in [[Scouting Domains]].
5. **Link, then verify.** `librarian index`, `views`, `integrity`, `pytest`, `eval`,
   `scenario`.

## The Limit — read this before trusting any note in this cohort

**No source file, notebook, README or documentation page from any of the 49 repositories
was opened.** The evidence base is: GitHub metadata, the complete file tree at HEAD, and —
for seventeen of them — licence files, read in full.

This is a **weaker** evidence base than the 2026-09-03 cohort, where several repositories
had source and documentation read directly. The two cohorts are *not* at equal depth, and
anyone comparing a claim from one against a claim from the other should know which is
which. Concretely:

- Statements about **what is in a repository** — directory structure, file counts,
  proportions, what exists and what does not — are strong. They come from a complete
  listing at a known commit.
- Statements about **how something works internally** are inference from names,
  proportions and the project's own description. Every such claim in a note is marked
  `**Not read:**` in `## Architecture & Mechanics`, which names exactly what was inferred
  rather than confirmed.
- Statements a project makes about **itself** — benchmark results, performance claims,
  positioning against alternatives — are recorded as claimed and were not checked. The
  clearest case is [[jgravelle - jcodemunch-mcp]], whose 95%-token-reduction figure is its
  own marketing; the benchmark tree behind it is unusually substantial and none of it was
  opened.

The file tree turns out to carry more than expected, and several notes rest on it entirely:
that [[hamelsmu - code_search]] is 97% vendored fastai, that
[[alexandershaw4 - PyBP-Py-BrainPlotter-for-AAL90]] is 94% vendored nibabel, that
[[rudradesai200 - SimpleFS]] is 90% generated Doxygen, that
[[ardamavi - Unsupervised-Classification-with-Autoencoder]] is 1,399 photographs and two
notebooks. None of those is visible from any description of the project, and each of them
changes what the source is for.

## What The Cohort Changed In The System

- **A new topic and a new axis value.** [[Topic - Data Lineage & Provenance]] was promoted
  from the register with eight resources, and `Data_Lineage` added to `domain_primary` in
  [[Note Content Model]] with the reasoning recorded there. [[recipy - recipy]] and
  [[shenhuan2021 - gudu-sql-omni-introduce]] moved into it.
- **Seven patterns and fourteen glossary terms**, each written because several sources in
  the cohort share it. A term appearing in one note is a word, not an entry.
- **A YAML defect in the note generator.** A backslash in a GitHub description
  (`Conceptual Search\Semantic Search`) broke a double-quoted scalar and failed
  `frontmatter_parses`. Fixed by escaping rather than by rewriting the value, because
  `github_description` records what the API returned.
- **A retrieval defect found, fixed and measured.** See [[Service Map]]. The eval never
  moved (MRR 0.94); the scenario test fell from 0.93 to 0.87 on `useful@5`. Part of that is
  displacement — 47 new notes competing for five slots — and part was a real defect:
  `SELECTIVITY_CEILING` is a fixed share of a corpus that keeps growing, so `files`, `test`,
  `file` and `read` all crossed it. Raised from 0.34 to 0.50 after a sweep against both
  instruments, recovering `useful@5` to 0.90 and cross-domain to 0.60 at no cost to the eval.
  Inverse-document-frequency weighting was tried alongside it, lost at every ceiling, and was
  rejected with the reasoning recorded in `consult._selective_terms`.
- **A licence policy corrected in scope.** `usage.distribution_posture` is now `private`,
  because nothing built with this catalogue is published. `scout.rank.reusability` had been
  scoring an unlicensed source a hard `0.0` under a 15-point weight — which removed twelve
  of this cohort from contention on the strength of an obligation that cannot arise. Every
  result now carries `permitted_uses` (`donor`, `reference`, `tool`), which is the question
  actually being asked. The licence *readings* are unchanged; only their consequence is.

## What Was Not Done

- **No scenario covers this cohort's subject matter.** All thirty scenarios were written
  against the 81-resource corpus, so none asks about lineage, parsing, retrieval or
  ontology design. The measured fall is real; the measured *coverage* is of the old corpus
  only.
- **Two licence readings still want a person**, recorded in
  [[Licence Resolution 2026-09-03]] — but under the `private` posture they block nothing,
  so that list is now a debt register for the day the posture changes rather than a queue.
- **Nothing was executed.** No fetched code was run, and every clone was deleted after its
  tree was listed.

## Related
- [[Scouting Working File 2026-09-03]] — the first cohort, read at greater depth
- [[Source Documentation Standard]] — the obligation these notes are written against
- [[Note Content Model]] — the schema, and the `Data_Lineage` addition
- [[Licence Resolution 2026-09-03]] — what a person still has to confirm
- [[Service Map]] — what the scenario test measured before and after
- [[Master Index]]
