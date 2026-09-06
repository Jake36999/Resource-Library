---
uuid: "51f73606-63e5-56e6-ac07-49cad6c75497"
canonical_url: "https://github.com/NorskRegnesentral/skweak"
repo_key: "NorskRegnesentral/skweak"
owner: "NorskRegnesentral"
repo_name: "skweak"
aliases: ["NorskRegnesentral/skweak", "https://github.com/NorskRegnesentral/skweak"]
type: "ml_framework"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Knowledge Management"]
ecosystem: "Python"
domain_primary: "ML_Training"
maturity_stage: "Abandoned"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: ["Programmatic Labelling"]
glossary_terms: ["Weak Supervision", "Labelling Function", "Named Entity Recognition"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "skweak: A software toolkit for weak supervision applied to NLP tasks"
github_language: "Python"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 926
github_topics: ["data-science", "distant-supervision", "natural-language-processing", "nlp-library", "nlp-machine-learning", "python", "spacy", "training-data", "weak-supervision"]
github_homepage: "Unknown"
github_pushed_at: "2024-09-02T12:48:05Z"
---
# NorskRegnesentral - skweak

## Bottom Line
Weak supervision for **spans** rather than whole examples: labelling functions mark text spans in spaCy documents, and an HMM aggregator reconciles them while modelling the dependence between neighbouring tokens that a per-example vote cannot see.

## What It Solves
- Build named-entity training data for a language or domain with no annotated corpus — its own examples are English CoNLL/MUC-6 and Norwegian sentiment.
- Aggregate conflicting span annotations into one layer without hand adjudication.
- Propagate a decision across a document, so a bare surname inherits the evidence from the full name mentioned eight paragraphs earlier.

## Architecture & Mechanics
- Annotators (`heuristics.py`: function, regex, token- and span-constraint, editor, vicinity; `gazetteers.py`: a trie over large dictionaries) mark spans on spaCy `Doc` objects.
- Aggregation is split along two independent axes: **shape** of the label space (`TextAggregatorMixin`, `SequenceAggregatorMixin`, `MultilabelAggregatorMixin`) and **method** (`voting.py` majority, or `generative.py` NaiveBayes and HMM fitted by EM).
- The HMM is the substantive difference from instance-level weak supervision: it models transitions between adjacent token labels rather than treating each token independently.
- `doclevel.py` adds `DocumentHistoryAnnotator` and `DocumentMajorityAnnotator`, which carry a decision across a whole document.

## What Is Inside
- **The library** — `skweak/`: `base.py` (annotator hierarchy), `heuristics.py` (function,
  regex, token-constraint, span-constraint, editor and vicinity annotators), `gazetteers.py`
  (a trie plus dictionary annotator), `aggregation.py` (label-space shape as mixins),
  `voting.py` (majority), `generative.py` (NaiveBayes, HMM, and multilabel variants),
  `doclevel.py` (document-history and document-majority propagation), `analysis.py`.
- **Two complete worked pipelines** — `examples/ner/` (CoNLL-2003 and MUC-6, with preparation
  and evaluation utilities) and `examples/sentiment/` (Norwegian NoReC, with lexicon and
  transformer models).
- **Bundled lexicons and corpora** — `data/`: Crunchbase companies, first names, geonames,
  products, a tokenised Wikidata subset, a small Reuters archive, and Norwegian sentiment
  lexicons (IBM Debater, NRC Emotion, NRC VAD, SoCaL, norsentlex).
- **Step-by-step notebooks** — `examples/quick_start.ipynb`, `examples/ner/Step by step NER.ipynb`,
  `examples/sentiment/Step_by_step.ipynb`.
- **Not here:** the documentation. It lives in the GitHub Wiki, outside the repository.

## Transferable Capability
**Separate two decisions that are usually tangled: what shape of thing you are judging, and how you reconcile disagreement about it.** One axis covers whether the judgement applies to a whole item, to a position in a sequence, or to several overlapping labels at once; the other covers whether conflicts are settled by counting or by modelling the judges. Either can be changed without touching the other.

The substantive addition is that **when judgements are adjacent, they are not independent** — what was decided next door constrains what is plausible here — and a reconciler that ignores that discards real information. A related move: **let a decision made once propagate across a whole document**, so a later, weaker occurrence inherits the evidence of an earlier, stronger one.

**Alternative to:** reconciliation that treats every position as an isolated case. **Applies wherever** decisions come in sequences or share context — and as a design lesson wherever two orthogonal choices have been fused into one implementation.

## Taxonomy
- Ecosystem: Python
- Domain Primary: ML_Training
- Maturity Stage: Abandoned
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Bootstrap NER for a low-resource language.
- Borrow the aggregator split — label-space shape and reconciliation method as separate choices — for any multi-voter labelling problem.
- Read the HMM aggregator as a worked example of sequence-aware label reconciliation.

## Reading Notes
**Unmaintained, by its authors' own statement.** The README reads: "Skweak is no longer actively maintained (if you are interested to take over the project, give us a shout)." Last push 2024-09-02. It has an ACL 2021 system-demonstration paper behind it and the code is complete, but nobody is fixing it, and the documentation lives in the GitHub Wiki rather than the repository.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [related_to:: [[urchade - GLiNER]]]
- [implements_pattern:: [[Pattern - Programmatic Labelling]]]
- [mentions_term:: [[Glossary - Weak Supervision]]]
- [mentions_term:: [[Glossary - Labelling Function]]]
- [mentions_term:: [[Glossary - Named Entity Recognition]]]

## Evidence
- Source URL: https://github.com/NorskRegnesentral/skweak
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: skweak: A software toolkit for weak supervision applied to NLP tasks
- Language: Python
- License (SPDX): MIT
- Default Branch: main
- Stars: 926
- Homepage: Unknown
- Pushed At: 2024-09-02T12:48:05Z
- Topics: data-science, distant-supervision, natural-language-processing, nlp-library, nlp-machine-learning, python, spacy, training-data, weak-supervision

## Evidence Anchors
- [github_repo] description :: skweak: A software toolkit for weak supervision applied to NLP tasks (confidence 0.95)
- [github_repo] language :: Python (confidence 0.90)
- [github_repo] license :: MIT (confidence 0.90)
- [github_repo] topics :: data-science, distant-supervision, natural-language-processing, nlp-library, nlp-machine-learning, python, spacy, training-data, weak-supervision (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
