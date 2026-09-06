---
uuid: "349a3cb8-c160-51a4-bc7f-bbe5c2783900"
canonical_url: "https://github.com/polkadot-java/api"
repo_key: "polkadot-java/api"
owner: "polkadot-java"
repo_name: "api"
aliases: ["polkadot-java/api", "https://github.com/polkadot-java/api"]
type: "developer_tool"
primary_topic: "Data APIs & Big Data"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Mixed"
domain_primary: "Data"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Server"
interface_protocol: "REST"
data_locality: "Distributed"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Schema-First Codegen", "ETL API Ingestion", "Reference Architecture"]
glossary_terms: ["API", "Schema", "Endpoint", "Async"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Apache-2.0"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 5
github_description: "Java APIs around Polkadot and any Substrate-based chain RPC calls. It is dynamically generated based on what the Substrate runtime provides in terms of metadata.Full documentation & examples available."
github_language: "Java"
github_license_spdx: "Apache-2.0"
github_default_branch: "master"
github_stars: 64
github_homepage: "https://polkadot-java.github.io/"
github_pushed_at: "2021-09-08T10:21:55Z"
---
# polkadot-java - api

## Bottom Line
A Java client whose type system is generated from metadata the server publishes at runtime rather than written against a fixed specification — the answer to a protocol that changes its own shape on upgrade, kept honest by dated bundles of runnable examples.

## What It Solves
- Call a service whose available methods and types change when the server upgrades.
- Avoid hand-maintaining client types against a moving target.
- Reproduce an example from a specific date, when the chain it ran against has since changed.

## Architecture & Mechanics
- The generative approach is the design: the runtime publishes metadata describing its own types and calls, and the client builds its type surface from that, so a server upgrade does not require a client release.
- **Examples are dated bundles, each self-contained** — `examples_runnable/20190511`, `20190518`, `20190525`, `20190601`, `20190616`, five snapshots two to three weeks apart, each shipping its own `polkadot-java-1.0-SNAPSHOT.jar`. Pinning the library inside the example is what makes a dated example still runnable.
- Generated Javadoc is committed — `doc/` is 606 of 1,190 files, produced by `gendoc.sh` — so the API surface is browsable in the repository.
- Native cryptography is included as source and binaries: `sr25519/cpp`, `sr25519/java`, `sr25519/libs`, with `.wasm` and `.dylib` artefacts in-tree.
- **Not read:** any Java source or example. The above is read off the tree, the dated directory names and the repository's stated purpose.

## What Is Inside
- **Five dated runnable example bundles** — `examples_runnable/`, 239 files, each with its own pinned jar. **The most transferable artefact here**: a worked answer to keeping examples runnable against a moving backend.
- **Committed generated Javadoc** — `doc/` (606 files, 620 HTML), with `doc/docfiles/examples/promise/` walking twenty numbered scenarios: `01_simple_connect`, `02_listen_to_blocks`, `03_listen_to_balance_change`, `04_unsubscribe`, `05_read_storage`, `06_make_transfer`.
- **Native cryptography** — `sr25519/` with C++ and Java bindings, prebuilt `.wasm`, `.dylib` and `.h` artefacts.
- **185 committed `.jar` files** — dependencies and snapshots in the tree, which is what makes this a 23 MB repository.
- **Not here:** any Substrate node. Every example needs one to connect to.

## Transferable Capability
**Generate the client from what the server says about itself, and pin the library inside every dated example.** Two independent ideas. The first: when a protocol's own shape is data the server publishes, a client can adapt without a release — which trades compile-time type safety for surviving upgrades, and is the right trade only when the server changes faster than the client can be republished. The second is smaller and more widely applicable: **an example that pins its dependencies inside its own directory stays runnable**, so a reader can reproduce a result from three years ago rather than discovering that the sample was written against a version nobody can obtain. Dating the bundle makes the drift visible instead of silent.

**Alternative to:** a hand-written client against a published specification, which is type-safe and breaks on upgrade; and to a single examples directory tracking HEAD, where every example is correct only until the next release. **Applies wherever** a client must survive an evolving server, or examples must remain reproducible across releases — an argument that applies to documentation, tutorials and benchmark harnesses equally.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Data
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Server
- Interface Protocol: REST
- Data Locality: Distributed
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Copy the dated, dependency-pinned example bundle scheme for any project whose examples must stay runnable.
- Read it as a worked case of runtime-metadata-driven client generation before hand-writing types for a moving API.
- Study the twenty numbered `promise/` scenarios as a progression from connecting to transacting.

## Reading Notes
**Last pushed 2021-09-08 and the newest examples are dated mid-2019.** Substrate has changed comprehensively since, so this will not work against a current chain and is not a live option. It is catalogued for the two portable mechanisms — runtime-metadata client generation and dated, self-contained example bundles — both of which are independent of blockchains entirely. Note also that the repository commits 185 jar files and prebuilt native binaries; that is why it is 23 MB, and it is a practice worth understanding before copying.

## Semantic Links
- [parent_topic:: [[Topic - Data APIs & Big Data]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[public-apis - public-apis]]]
- [related_to:: [[NatLabRockies - api-umbrella]]]
- [related_to:: [[open-metadata - OpenMetadata]]]
- [implements_pattern:: [[Pattern - Schema-First Codegen]]]
- [implements_pattern:: [[Pattern - ETL API Ingestion]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [mentions_term:: [[Glossary - API]]]
- [mentions_term:: [[Glossary - Schema]]]
- [mentions_term:: [[Glossary - Endpoint]]]
- [mentions_term:: [[Glossary - Async]]]

## Evidence
- Source URL: https://github.com/polkadot-java/api
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata, the complete file tree at HEAD, and the LICENSE file; no Java source, example or generated document was opened

## GitHub Snapshot

- Description: Java APIs around Polkadot and any Substrate-based chain RPC calls. It is dynamically generated based on what the Substrate runtime provides in terms of metadata.Full documentation & examples available.
- Language: Java
- License (SPDX): Apache-2.0
- Default Branch: master
- Stars: 64
- Homepage: https://polkadot-java.github.io/
- Pushed At: 2021-09-08T10:21:55Z

## Evidence Anchors
- [github_repo] description :: Java APIs around Polkadot and any Substrate-based chain RPC calls. It is dynamically generated based on what the Substrate runtime provides in terms of metadata.Full documentation & examples available. (confidence 0.95)
- [github_repo] language :: Java (confidence 0.90)
- [github_repo] license :: Apache-2.0 (confidence 0.90)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 1190 paths at HEAD (confidence 0.95)
