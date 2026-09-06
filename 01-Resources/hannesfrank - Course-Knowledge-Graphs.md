---
uuid: "462e4db4-74db-5f95-a23b-262d11c8d437"
canonical_url: "https://github.com/hannesfrank/Course-Knowledge-Graphs"
repo_key: "hannesfrank/Course-Knowledge-Graphs"
owner: "hannesfrank"
repo_name: "Course-Knowledge-Graphs"
aliases: ["hannesfrank/Course-Knowledge-Graphs", "https://github.com/hannesfrank/Course-Knowledge-Graphs"]
type: "dataset"
primary_topic: "Knowledge Management"
secondary_topics: []
ecosystem: "Python"
domain_primary: "Knowledge_Management"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Knowledge Graph Routing"]
glossary_terms: ["Knowledge Graph", "Community Detection", "Dataset"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Test data and example source code for the Knowledge Graphs lecture 2018"
github_language: "Python"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 0
github_homepage: "https://iccl.inf.tu-dresden.de/web/Knowledge_Graphs_(WS2018)/en"
github_pushed_at: "2018-10-17T11:54:18Z"
---
# hannesfrank - Course-Knowledge-Graphs

## Bottom Line
Seven small graph test files from a 2018 university knowledge-graphs course, ordered from a triangle to a random medium graph — a graded fixture set for checking that a graph algorithm is correct before it is fast.

## What It Solves
- Verify a graph algorithm on inputs whose answers can be computed by hand.
- Have a size progression, so a failure can be localised to scale rather than to logic.
- Get test data for graph work without generating or licensing a corpus.

## Architecture & Mechanics
- The numbering is the design: `01-triangle`, `02-empty`, `03-k5`, `04-s5`, `05-random-small`, `06-random-medium`. Each name states the graph, so an unexpected result is immediately attributable to a known shape.
- The first four are structures with known properties — a triangle, the empty graph, the complete graph on five vertices, the star on five — which means the expected output is derivable rather than recorded.
- `02-empty` is the degenerate case, present at position two: the input most implementations crash on, tested before anything interesting.
- One script under `scripts/`; the repository is otherwise entirely data.
- **Not read:** the files' contents or the script. The graph identities above are read from the filenames, which use standard notation.

## What Is Inside
- **Seven graph files** — `test-data/`: `01-triangle.txt`, `02-empty.txt`, `03-k5.txt`, `04-s5.txt`, `05-random-small.txt`, `06-random-medium.txt`.
- **One script** — `scripts/`, presumably a generator or loader.
- **Ten paths in total.** The homepage points at the TU Dresden Knowledge Graphs course, winter semester 2018.
- **Not here:** any algorithm, any documentation beyond the README, or any licence.

## Transferable Capability
**Order your fixtures from hand-checkable to realistic, and name each one by the property it tests.** Four structures with known answers, then two random graphs, means a failure is attributable the moment it happens: a wrong result on `k5` is a logic error, a wrong result only on `random-medium` is a scale or assumption error. Putting the **degenerate case second** is the specific discipline worth copying — the empty input is where most implementations fail and where almost no fixture set starts. Naming by property rather than by number alone is what makes the set usable by someone who did not build it.

**Alternative to:** one large realistic input, which tells you something is wrong and not what; and to randomly generated fixtures alone, where there is no independent answer to check against. **Applies wherever** an algorithm's correctness must be separated from its behaviour at scale.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Knowledge_Management
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Use the seven files directly as a first test set for any graph traversal, centrality or community algorithm.
- Copy the naming-and-ordering scheme when building fixtures for anything with a degenerate case.
- Reach for it when validating graph tooling that will later run against a real corpus.

## Reading Notes
**No licence and none reported by GitHub**, so it is excluded from licence-constrained answers — though for six tiny generated graph files the practical risk is low, the catalogue's rule does not make exceptions on size. Zero stars, last pushed 2018-10-17, course material rather than a project. Catalogued because a graded fixture set is genuinely reusable and rarely published; its value is entirely in the shape of the collection, not in its size.

## Semantic Links
- [parent_topic:: [[Topic - Knowledge Management]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[neo4j-labs - neocarta]]]
- [related_to:: [[mdebellis - SemanticKG-Design]]]
- [related_to:: [[JayLZhou - GraphRAG]]]
- [implements_pattern:: [[Pattern - Knowledge Graph Routing]]]
- [mentions_term:: [[Glossary - Knowledge Graph]]]
- [mentions_term:: [[Glossary - Community Detection]]]
- [mentions_term:: [[Glossary - Dataset]]]

## Evidence
- Source URL: https://github.com/hannesfrank/Course-Knowledge-Graphs
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no data file or script was opened, and no licence file exists to read

## GitHub Snapshot

- Description: Test data and example source code for the Knowledge Graphs lecture 2018
- Language: Python
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 0
- Homepage: https://iccl.inf.tu-dresden.de/web/Knowledge_Graphs_(WS2018)/en
- Pushed At: 2018-10-17T11:54:18Z

## Evidence Anchors
- [github_repo] description :: Test data and example source code for the Knowledge Graphs lecture 2018 (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 10 paths at HEAD (confidence 0.95)
