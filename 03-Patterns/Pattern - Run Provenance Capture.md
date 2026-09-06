---
pattern_key: "run_provenance_capture"
aliases: ["automatic provenance logging"]
type: "pattern"
status: "active"
examples: ["recipy - recipy"]
glossary_terms: ["Provenance", "Data Lineage", "Dataset"]
topic_keys: ["data_lineage_provenance"]
---

# Pattern - Run Provenance Capture

## Definition
Record what produced each output file — the script, the arguments, the code version, the environment, the inputs — automatically at run time by intercepting the library calls that read and write files, rather than asking the author to declare it.

## Why It Matters
- Provenance that must be declared does not get declared. Capture at the point of I/O is the only version that survives contact with an ordinary working day.
- Identifying artefacts by content hash rather than by path means provenance survives a rename, a copy or a transfer to a colleague.
- The approach is bounded by its interception surface: it can only see the libraries it has patched, so coverage is a list that ages.

## Example Repositories
- [[recipy - recipy]]

## Related Glossary
- [[Glossary - Provenance]]
- [[Glossary - Data Lineage]]
- [[Glossary - Dataset]]

## Related Topics
- [[Topic - Data APIs & Big Data]]
