---
uuid: "784b3925-b2ba-54f5-b8ce-14aa5df9d8c0"
canonical_url: "https://github.com/rudradesai200/SimpleFS"
repo_key: "rudradesai200/SimpleFS"
owner: "rudradesai200"
repo_name: "SimpleFS"
aliases: ["rudradesai200/SimpleFS", "https://github.com/rudradesai200/SimpleFS"]
type: "reference_implementation"
primary_topic: "Architecture & Developer Playbooks"
secondary_topics: ["Infrastructure & Observability"]
ecosystem: "Mixed"
domain_primary: "Infrastructure"
maturity_stage: "Reference"
license_class: "Unknown"
deployment_target: "Local_Only"
interface_protocol: "CLI"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Reference Architecture", "System Design Reference"]
glossary_terms: ["Architecture", "System Design", "Scalability"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "Unknown"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-04"
evidence_count: 6
github_description: "The file system is a layer of abstraction between the storage medium and the operating system. In the absence of a file system, it is tough to retrieve and manage data stored in the storage media. File systems provide an interface to access and control the data. It is implemented by separating data into chunks of predetermined size and labeling them for better management and operability. There are several types of file systems available out there. Some major examples are as follows: Disk-Based, Network-Based, and Virtual based."
github_language: "C++"
github_license_spdx: "NOASSERTION"
github_default_branch: "master"
github_stars: 7
github_topics: ["filesystem", "linux", "os", "unix"]
github_homepage: "https://rudradesai200.github.io/SimpleFS/"
github_pushed_at: "2023-05-20T22:12:38Z"
---
# rudradesai200 - SimpleFS

## Bottom Line
A file system implemented from scratch in five C++ files, with a shell to drive it and ten shell scripts that test it operation by operation — small enough to read completely, which is the entire point of it.

## What It Solves
- Understand what a file system is by reading one rather than a chapter about one.
- See inode allocation, block management and directory structure implemented rather than described.
- Exercise each operation independently, so a failure names the operation.

## Architecture & Mechanics
- Five implementation files: `src/library/` (4) and `src/shell/` (1), with the public interface in `include/sfs/` (3). A file system in nine source files.
- The separation of library from shell matters: the file system is a library with an interface, and the shell is one consumer of it — so the abstraction boundary is real rather than notional.
- Tests are one shell script per operation — `test_format.sh`, `test_create.sh`, `test_cat.sh`, `test_copyin.sh`, `test_copyout.sh`, `test_debug.sh` — which is exactly the granularity that makes a failure attributable.
- `fsconfig.dox` and a `Makefile` at the root: Doxygen generates the documentation, and the generated output is committed.
- **Not read:** any C++ source. The layering above is read off directory names and file counts.

## What Is Inside
- **A complete file system in nine files** — `src/library/` (4), `src/shell/` (1), `include/sfs/` (3), plus a `Makefile`.
- **Ten per-operation test scripts** — `tests/`: format, create, cat, copyin, copyout, debug and more, one shell script each.
- **250 files of generated Doxygen HTML** — `docs/`, including a 117-file search index. **Ninety per cent of this repository is generated documentation**, committed so that GitHub Pages can serve it; the source is nine files.
- **`data/`** — three disk images to operate on.
- **Not here:** a licence, any concurrency, journalling or crash recovery. It is a teaching artefact and does not pretend otherwise.

## Transferable Capability
**Implement the thing at a size a person can hold in their head, and test one operation per test.** A file system is usually encountered as either a textbook chapter, which cannot be run, or a production kernel subsystem, which cannot be read; the useful middle is a complete implementation small enough to finish. **One test per operation** is the accompanying discipline that makes such an artefact usable for learning — a failing test names the operation, so the reader is pointed at the concept rather than at a stack trace.

The practice *not* to copy is visible in the same tree: committing 250 files of generated documentation to serve a GitHub Pages site makes the repository ten times its real size and makes every diff unreadable.

**Alternative to:** reading a production file system, which is complete and impenetrable; and to a textbook, which is clear and cannot be executed. **Applies wherever** a concept is best learned from a complete small instance — schedulers, allocators, interpreters, protocols, databases.

## Taxonomy
- Ecosystem: Mixed
- Domain Primary: Infrastructure
- Maturity Stage: Reference
- License Class: Unknown
- Deployment Target: Local_Only
- Interface Protocol: CLI
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read it end to end to understand inode allocation and block management concretely.
- Copy the one-test-per-operation scheme for any teaching implementation.
- Use it as a base for adding a feature it deliberately omits — journalling, for instance — as an exercise.

## Reading Notes
**No licence file and none reported by GitHub**, so it is excluded from licence-constrained answers; read it, do not lift from it. Seven stars, created 2020-11-06, a student project — which is the correct frame: it is teaching material, and it omits concurrency, journalling and crash recovery entirely. Note the shape before cloning: **250 of 278 files are generated Doxygen output**, so every count of this repository overstates it by an order of magnitude.

## Semantic Links
- [parent_topic:: [[Topic - Architecture & Developer Playbooks]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[donnemartin - system-design-primer]]]
- [related_to:: [[hhstore - annotated-py-projects]]]
- [related_to:: [[ByteByteGoHq - system-design-101]]]
- [implements_pattern:: [[Pattern - Reference Architecture]]]
- [implements_pattern:: [[Pattern - System Design Reference]]]
- [mentions_term:: [[Glossary - Architecture]]]
- [mentions_term:: [[Glossary - System Design]]]
- [mentions_term:: [[Glossary - Scalability]]]

## Evidence
- Source URL: https://github.com/rudradesai200/SimpleFS
- Source kind: GitHub REST metadata plus the repository tree, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-04
- Depth of read: GitHub metadata and the complete file tree at HEAD; no C++ source or test script was opened, and no licence file exists to read

## GitHub Snapshot

- Description: The file system is a layer of abstraction between the storage medium and the operating system. In the absence of a file system, it is tough to retrieve and manage data stored in the storage media. File systems provide an interface to access and control the data. It is implemented by separating data into chunks of predetermined size and labeling them for better management and operability. There are several types of file systems available out there. Some major examples are as follows: Disk-Based, Network-Based, and Virtual based.
- Language: C++
- License (SPDX): NOASSERTION
- Default Branch: master
- Stars: 7
- Homepage: https://rudradesai200.github.io/SimpleFS/
- Pushed At: 2023-05-20T22:12:38Z
- Topics: filesystem, linux, os, unix

## Evidence Anchors
- [github_repo] description :: The file system is a layer of abstraction between the storage medium and the operating system. In the absence of a file system, it is tough to retrieve and manage data stored in the storage media. File systems provide an interface to access and control the data. It is implemented by separating data into chunks of predetermined size and labeling them for better management and operability. There are several types of file systems available out there. Some major examples are as follows: Disk-Based, Network-Based, and Virtual based. (confidence 0.95)
- [github_repo] language :: C++ (confidence 0.90)
- [github_repo] license :: NOASSERTION (confidence 0.90)
- [github_repo] topics :: filesystem, linux, os, unix (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-04 (confidence 0.95)
- [repository_tree] file count :: 278 paths at HEAD (confidence 0.95)
