---
type: "operational_record"
status: "active"
created: "2026-09-03"
examined: 69
resolved: 44
needs_review: 10
purpose: "what the licence backfill changed, and what a person still has to confirm"
---

# Licence Resolution 2026-09-03

## Why This Ran

`license_class` is the one field that **eliminates** in `find_donor`: a resource whose
licence is `Unknown` is not offered as a lower-ranked answer to a permissive-only query,
it is not an answer at all. 52 of the catalogue's 81 resources carried `Unknown`,
not because they are unlicensed but because the GitHub API reports `NOASSERTION` or nothing
for every composite LICENSE, every source-available licence, and every repository that
states its licence somewhere other than a recognised file.

The resolver added in [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]
reads the LICENSE directly. This note records what it changed.

## What Changed

**41 notes rewritten.** `license` and `license_class` now hold what the licence
text says. `github_license_spdx` was **left alone** - it records what the API returned, and
the `## Evidence Anchors` block quotes it. The disagreement between the two fields is the
finding, not an inconsistency to tidy away.

No frontmatter field was added. Review status lives in this note rather than in the notes,
because adding a field would be schema drift (`NO_SCHEMA_DRIFT`).

## A Defect The Run Found, And What It Cost

The first version of the resolver inferred a licence *choice* from wording as well as from
an SPDX expression, using phrases including `either version`. That phrase is GPL and AGPL
boilerplate - "either version 3 of the License, or (at your option) any later version"
appears in every copy of those licences - and it describes a choice between **versions of
one licence**, not between licences.

The effect was to take the *least* restrictive name in a composite instead of the most.
Two resources came back wrong, and both in the dangerous direction:

| Resource | Reported | Correct |
| --- | --- | --- |
| [[ckan - ckan]] | Permissive | **Copyleft** (AGPL-3.0) |
| [[wazuh - wazuh]] | Permissive | **Copyleft** (GPL-2.0) |

A copyleft project offered as an answer to a permissive-only query is the one error this
field must never make - it is worse than the `Unknown` it replaced, because `Unknown` is
merely unhelpful while this is confidently wrong. The two were caught by reading the run's
output before applying it, not by a test.

The rule now infers a choice **only** from an explicit `SPDX-License-Identifier` expression
containing `OR`, which is machine-readable and unambiguous. Prose is read for *which*
licences are present, never for how they combine. `scout/tests/test_rank.py` pins it.

The corrected classes were recomputed offline from the licence names already captured, so
no repository was fetched twice.

## Settled - read from a LICENSE, single licence, no ambiguity

| Resource | Repository | Licence | Class | Read from |
| --- | --- | --- | --- | --- |
| [[alphagov - whitehall]] | `alphagov/whitehall` | MIT | Permissive | LICENSE |
| [[astropy]] | `astropy/astropy` | BSD-3-Clause | Permissive | LICENSE |
| [[awslabs - awsome-distributed-ai]] | `awslabs/awsome-distributed-ai` | MIT | Permissive | LICENSE |
| [[Azure-Samples - semantic-kernel-advanced-usage]] | `Azure-Samples/semantic-kernel-advanced-usage` | MIT | Permissive | LICENSE |
| [[CadQuery - cadquery]] | `CadQuery/cadquery` | Apache-2.0 | Permissive | LICENSE |
| [[cfpb - open-source-checklist]] | `cfpb/open-source-checklist` | CC0-1.0 | Permissive | LICENSE |
| [[chef]] | `chef/chef` | Apache-2.0 | Permissive | LICENSE |
| [[donnemartin - system-design-primer]] | `donnemartin/system-design-primer` | CC-BY-4.0 | Permissive | LICENSE |
| [[G-Research - siembol]] | `G-Research/siembol` | Apache-2.0 | Permissive | LICENSE |
| [[gap-system - gap]] | `gap-system/gap` | GPL-2.0 | Copyleft | LICENSE |
| [[GSA - data.gov]] | `GSA/data.gov` | CC0-1.0 | Permissive | LICENSE |
| [[hhstore - annotated-py-projects]] | `hhstore/annotated-py-projects` | MIT | Permissive | LICENSE |
| [[LaurentRDC - scikit-ued]] | `LaurentRDC/scikit-ued` | GPL-3.0 | Copyleft | LICENSE |
| [[markusschanta - awesome-jupyter]] | `markusschanta/awesome-jupyter` | CC-BY-SA-4.0 | Copyleft | LICENSE |
| [[Modernizr]] | `Modernizr/Modernizr` | MIT | Permissive | LICENSE |
| [[NatLabRockies - api-umbrella]] | `NatLabRockies/api-umbrella` | MIT | Permissive | LICENSE |
| [[necolas - normalize.css]] | `necolas/normalize.css` | MIT | Permissive | LICENSE |
| [[netdata]] | `netdata/netdata` | GPL-3.0 | Copyleft | LICENSE |
| [[ngageoint - geoq]] | `ngageoint/geoq` | MIT | Permissive | LICENSE |
| [[openscad - openscad]] | `openscad/openscad` | GPL-2.0 | Copyleft | LICENSE |
| [[openstack]] | `openstack/openstack` | Apache-2.0 | Permissive | LICENSE |
| [[orsinium-labs - generated-awesomeness]] | `orsinium-labs/generated-awesomeness` | CC0-1.0 | Permissive | LICENSE |
| [[prometheus]] | `prometheus/prometheus` | Apache-2.0 | Permissive | LICENSE |
| [[puppetlabs - puppet]] | `puppetlabs/puppet` | Apache-2.0 | Permissive | LICENSE |
| [[react]] | `react/react` | MIT | Permissive | LICENSE |
| [[scadastrangelove - awesome-ai-security-tools]] | `scadastrangelove/awesome-ai-security-tools` | CC0-1.0 | Permissive | LICENSE |
| [[simbody]] | `simbody/simbody` | Apache-2.0 | Permissive | LICENSE |
| [[square - square.github.io]] | `square/square.github.io` | Apache-2.0 | Permissive | LICENSE |
| [[stac-utils - pystac]] | `stac-utils/pystac` | Apache-2.0 | Permissive | LICENSE |
| [[statsd]] | `statsd/statsd` | MIT | Permissive | LICENSE |
| [[The-Cool-Coders - Project-Ideas-And-Resources]] | `The-Cool-Coders/Project-Ideas-And-Resources` | MIT | Permissive | LICENSE |
| [[twbs - bootstrap]] | `twbs/bootstrap` | MIT | Permissive | LICENSE |
| [[vercel-labs - skills]] | `vercel-labs/skills` | MIT | Permissive | LICENSE |

## Needs A Person - composite, dual-licensed, or read from prose

These are resolved and written, but the reading involved a judgement a person should
confirm. A composite takes the **most restrictive** licence present, because that is what
binds a reuser. A dual licence declared with `OR` takes the **least** restrictive, because
the reuser may choose. Anything read from a readme rather than a LICENSE is weaker evidence
by construction.

| Resource | Repository | Licence | Class | Read from |
| --- | --- | --- | --- | --- |
| [[ckan - ckan]] | `ckan/ckan` | AGPL-3.0 AND BSD-3-Clause | Copyleft | LICENSE |
| [[github - government.github.com]] | `github/government.github.com` | CC0-1.0 | Permissive | readme |
| [[mhadidg - software-architecture-books]] | `mhadidg/software-architecture-books` | CC-BY-4.0 | Permissive | readme |
| [[OSGeo - gdal]] | `OSGeo/gdal` | Apache-2.0 AND BSD-3-Clause AND ISC AND MIT | Permissive | LICENSE |
| [[osquery - osquery]] | `osquery/osquery` | Apache-2.0 OR GPL-2.0 | Permissive | LICENSE |
| [[sympy]] | `sympy/sympy` | BSD-3-Clause AND MIT | Permissive | LICENSE |
| [[usds - playbook]] | `usds/playbook` | CC0-1.0 | Permissive | readme |
| [[wazuh - wazuh]] | `wazuh/wazuh` | BSD-2-Clause AND GPL-2.0 | Copyleft | LICENSE |

### Added by the second cohort, 2026-09-04

The same resolver ran over the seventeen sources in the 2026-09-04 cohort that GitHub
reported as `NOASSERTION` or nothing. Three resolved cleanly, two need a person, and the
remaining twelve are genuinely unlicensed and appear in the section below.

| Resource | Repository | Licence | Class | Read from |
| --- | --- | --- | --- | --- |
| [[javaparser - javaparser]] | `javaparser/javaparser` | LGPL-3.0 AND Apache-2.0 | Weak_Copyleft | LICENSE |
| [[awsdocs - amazon-comprehend-developer-guide]] | `awsdocs/amazon-comprehend-developer-guide` | CC-BY-SA-4.0 AND MIT | Copyleft | LICENSE, LICENSE-SUMMARY |

**[[javaparser - javaparser]] is the clearest case yet for keeping this list, and the
clearest cost of the rule that produced it.** Its `LICENSE` says, in plain prose, that the
project is available under *either* the LGPL or the Apache licence and that the user
chooses. That is an unambiguous dual licence, and the Apache half would satisfy almost any
reuse. The resolver did not act on it, because after the `either version` defect recorded
above it infers a choice **only** from an explicit SPDX `OR` expression - so javaparser is
classified at the more restrictive half and is currently excluded from every
permissive-constrained answer.

That is the conservative failure and it is the one this catalogue chose: a source wrongly
withheld is recoverable by a person reading two paragraphs, a source wrongly offered is
not recoverable at all. But it is a real cost, incurred twice now, and if a third case
appears the rule is worth revisiting - the honest fix is a `license_overrides` entry per
confirmed case, not a looser heuristic.

[[awsdocs - amazon-comprehend-developer-guide]] is a composite of a different kind: the
prose is CC-BY-SA-4.0 and the sample code is a modified MIT, so *which half you are reusing*
decides the answer. It is classified at the more restrictive half. Three resolved without
ambiguity and were written directly into their notes: [[mdebellis - SemanticKG-Design]]
(CC-BY-4.0), [[jgravelle - jcodemunch-mcp]] (MIT) and, from the first pass, nothing changed.

## Still Unknown - and correctly so

| Resource | Repository | Why |
| --- | --- | --- |
| [[armanakbari - Awsome-Efficient-DLMs]] | `armanakbari/Awsome-Efficient-DLMs` | no licence text found |
| [[ByteByteGoHq - system-design-101]] | `ByteByteGoHq/system-design-101` | LICENSE present but matched no known licence |
| [[DovAmir - awesome-design-patterns]] | `DovAmir/awesome-design-patterns` | readme present but matched no known licence |
| [[ganarajpr - awesome-dspy]] | `ganarajpr/awesome-dspy` | no licence text found |
| [[moyu6027 - awsome-chatgpt-like]] | `moyu6027/awsome-chatgpt-like` | no licence text found |
| [[nathansmith - 960-Grid-System]] | `nathansmith/960-Grid-System` | no licence text found |
| [[not-a-bank - open-banking-tracker-data]] | `not-a-bank/open-banking-tracker-data` | LICENSE present but matched no known licence |
| [[pracdata - awesome-open-source-data-engineering]] | `pracdata/awesome-open-source-data-engineering` | no licence text found |
| [[shenhuan2021 - gudu-sql-omni-introduce]] | `shenhuan2021/gudu-sql-omni-introduce` | no licence text found |
| [[SigmaHQ - sigma]] | `SigmaHQ/sigma` | LICENSE present but matched no known licence |
| [[alexandershaw4 - PyBP-Py-BrainPlotter-for-AAL90]] | `alexandershaw4/PyBP-Py-BrainPlotter-for-AAL90` | no licence text found |
| [[carter-kilgour - delta-quality-testing]] | `carter-kilgour/delta-quality-testing` | no licence text found |
| [[fighting41love - funNLP]] | `fighting41love/funNLP` | no licence text found - and it ships corpora |
| [[hannesfrank - Course-Knowledge-Graphs]] | `hannesfrank/Course-Knowledge-Graphs` | no licence text found |
| [[JackieZhangdx - WeakSupervisedSegmentationList]] | `JackieZhangdx/WeakSupervisedSegmentationList` | no licence text found |
| [[JayLZhou - GraphRAG]] | `JayLZhou/GraphRAG` | no licence text found |
| [[open-metadata - docs-v1-legacy]] | `open-metadata/docs-v1-legacy` | no licence text found - and it is 5,483 pages of prose |
| [[rudradesai200 - SimpleFS]] | `rudradesai200/SimpleFS` | no licence text found |
| [[soulbliss - NLP-conference-compendium]] | `soulbliss/NLP-conference-compendium` | no licence text found |
| [[stephanie-wang - lineage-stash-artifact]] | `stephanie-wang/lineage-stash-artifact` | no licence text found |
| [[thinktecture-labs - semantic-kernel-semanticsearch]] | `thinktecture-labs/semantic-kernel-semanticsearch` | no licence text found |
| [[whole-tale - provenance-examples]] | `whole-tale/provenance-examples` | no licence text found - and it redistributes third-party research data |
| [[Victor-Kipruto-Rop - medallion-lakehouse-platform]] | `Victor-Kipruto-Rop/medallion-lakehouse-platform` | no licence text found |

Twelve of the twenty-three above came from the 2026-09-04 cohort, which is a much higher
unlicensed rate than the first pass - a consequence of that cohort containing more small,
single-author and academic repositories, where publishing without a licence is normal and
is rarely deliberate. Three are worth singling out because the absence has teeth:
[[fighting41love - funNLP]] *contains* corpora rather than linking to them,
[[whole-tale - provenance-examples]] redistributes published third-party research data, and
[[open-metadata - docs-v1-legacy]] is 5,483 pages of prose with no stated terms at all.

An `Unknown` that survives this pass is a finding rather than a gap: the repository either
ships no licence at all, or ships one no lookup table recognises.

**What that costs changed on 2026-09-04, and the change was a correction of scope rather
than a relaxation of standards.** These readings were being used to answer a question
nobody here was asking. This catalogue serves one person's R&D on tooling that is not
published; nothing built with it is distributed. Under that posture reading a repository,
running it, and copying code out of it all trigger no obligation, whatever the licence says
- so `Unknown` scoring a hard zero in `scout.rank.reusability` was removing twelve sources
from serious contention on the strength of an obligation that cannot arise.

The question actually being asked is **can I use this as donor code, as a reference, or as
a tool** - and `usage.distribution_posture: "private"` in `library_config.json` now makes
the system answer that one. Every result carries `permitted_uses`, derived on read from the
recorded class plus the posture, and under `private` it is all three for every class.

**Nothing about the recording changed.** Every licence above is still read from the text,
still classified, still disagreeing with the API where it disagrees. The facts are what
survive a change of posture; the consequences are what do not. Set the posture to
`distributed` and the strict scale, the strict `permitted_uses` table and the
`reusability` zero all return in a single config edit - which is the point of putting the
decision in a config key rather than in the classifier.

## What To Do With This

**Under the current `private` posture this list is not blocking anything.** It is a debt
register for the day the posture changes, and the reason to keep it is that the day it
changes is exactly the day nobody will want to re-read forty-four LICENSE files.

Confirm the composites above by reading their LICENSE files. Where the resolver was wrong,
record the correct SPDX in `.utility/library_config.json` under `license_overrides`, which
the build already prefers over anything derived, and note who checked and when.
[[javaparser - javaparser]] is the one worth doing first: it is a genuine dual licence
whose permissive half is being ignored by a deliberately conservative rule.

## Related
- [[Research Report 2026-09-03 - Lineage, Parsing and Graph Reasoning]]
- [[Taxonomy Index]]
- [[Master Index]]
