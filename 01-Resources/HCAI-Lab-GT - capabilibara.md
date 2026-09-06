---
uuid: "1732ef42-cf29-580b-bf88-25ff9a841cbf"
canonical_url: "https://github.com/HCAI-Lab-GT/capabilibara"
repo_key: "HCAI-Lab-GT/capabilibara"
owner: "HCAI-Lab-GT"
repo_name: "capabilibara"
aliases: ["HCAI-Lab-GT/capabilibara", "https://github.com/HCAI-Lab-GT/capabilibara"]
type: "research_artifact"
primary_topic: "ML Training & MLOps"
secondary_topics: ["Agentic AI & Models"]
ecosystem: "Web_Frontend"
domain_primary: "ML_Training"
maturity_stage: "Reference"
license_class: "Copyleft"
deployment_target: "Server"
interface_protocol: "Web_UI"
data_locality: "Stateless"
hardware_footprint: "CPU_Only"
security_compliance: "Uncertified"
agent_surface: "None"
patterns: []
glossary_terms: ["Training Data Attribution", "Provenance", "LLM"]
status: "published"
maturity: "curated"
sensitivity: "normal"
license: "AGPL-3.0 (code); CC BY-SA 4.0 (website content)"
source_file: "repositories to chart.md"
ingestion_agent: "claude"
metadata_captured_at: "2026-09-03"
evidence_count: 5
github_description: "Training-data attribution as a discovery method for capability provenance in language models. COLM 2026."
github_language: "JavaScript"
github_license_spdx: "AGPL-3.0"
github_default_branch: "main"
github_stars: 7
github_topics: ["ai-research", "capability-provenance", "interpretability", "language-models", "machine-unlearning", "mechanistic-interpretability", "research", "training-data-attribution"]
github_homepage: "https://hcai-lab-gt.github.io/capabilibara/"
github_pushed_at: "2026-08-23T03:31:21Z"
---
# HCAI-Lab-GT - capabilibara

## Bottom Line
A paper and its project website, not the pipeline they describe: the attribution code for a COLM 2026 study on which regions of a pretraining corpus produce which reasoning capabilities is unreleased, and the `src/` tree the README documents does not exist in the repository.

## What It Solves
- For the research: asks which corpus regions a capability actually depends on, and tests the answer causally by unlearning those regions and measuring the damage.
- For the reader: supplies the method, the scale and the limitations in the paper and on the site.
- It does not currently solve anything for someone wanting to run attribution.

## Architecture & Mechanics
- What the repository contains: `public/` (a Bulma static site with GSAP animations), the paper PDF, a dev server, a deploy script, and `hf_space/` (a Gradio demo).
- What the README describes but does not ship: Dolma3 de-duplicated and classified into WebOrganizer's 24 topic × 24 format taxonomy, a 5.68M-document stratified working set over 576 bins, query gradients from OLMo3-7B Instruct against document gradients from OLMo3-7B Base, gradient-based attribution via TrackStar/Bergson, and influence-targeted versus matched-random unlearning with LoRA and NGDiff.
- Stated cost of the study: roughly 37K H200-equivalent GPU-hours.
- Released artefacts are to be aggregate bin-level statistics only; document-level attribution scores are withheld by design.

## What Is Inside
- **A paper** — `Capability_Provenance_in_Language_Models.pdf`, plus `CITATION.cff` and
  `public/static/capabilibara.bib`.
- **A project website** — `public/`: Bulma CSS, `index.html`, and animation JavaScript
  (`js/figure1.js`, `js/influence-anim.js`, `js/animations/socialtda-data.js`).
- **A Gradio demo** — `hf_space/app.py`, which renders heatmaps from `np.random.randn`, not
  from results.
- **Planning and design documents** — `docs/superpowers/plans/`, `docs/superpowers/specs/`,
  `docs/website-methodology-first-plan.md`.
- **Not here, and this is the point:** the attribution pipeline. The `src/` layout the README
  documents (`data_attribution/`, `dolma/`, `unlearning/`) does not exist in the tree.

## Transferable Capability
**Attribute a system's behaviour back to the material that produced it, and then test the attribution by removing that material and measuring what breaks.** The claim is only as good as the check: influence estimates are correlational, so the method pairs them with a deliberate removal and a measured consequence. The second, cheaper idea is **aggregation as the unit of analysis** — individual attributions are noisy, so group the material into comparable regions first and reason about regions.

**Alternative to:** explaining behaviour from the artefact alone, without reference to what produced it; and to trusting an attribution score with no causal check attached. **Applies wherever** an output must be traced to its inputs and the tracing needs to be believed — provenance, audit, or deciding which of several sources actually carried the result.

*The method is published; the implementation is not released.*

## Taxonomy
- Ecosystem: Web_Frontend
- Domain Primary: ML_Training
- Maturity Stage: Reference
- License Class: Copyleft
- Deployment Target: Server
- Interface Protocol: Web_UI
- Data Locality: Stateless
- Hardware Footprint: CPU_Only
- Security Compliance: Uncertified
- Agent Surface: None

## Integration & Use Cases
- Read the method and the limitations section before designing any attribution work.
- Watch the roadmap for the audited code port; there is nothing to run until then.
- Cite the paper (arXiv 2606.19625), not the repository.

## Reading Notes
Two findings recorded rather than the usual one. **The canonical location moved**: `eilab-gt/capabilibara` 301-redirects here, and the README's own clone command still points at the old path. **The public demo renders synthetic data with no user-visible disclaimer**: `hf_space/app.py` line 31 reads `# Generate synthetic influence baseline data matching paper distributions for 576 bins`, then `np.random.seed(42)` and `np.random.randn(24, 24)` with hand-applied offsets, while the Space's README advertises a Matrix Explorer over 576 corpus bins and an Influence Breakdown across four named benchmarks. The repository README is scrupulous that the code is unreleased; the demo is not scrupulous that the numbers are invented. AGPL-3.0 also puts this outside any permissive-only constraint.

## Semantic Links
- [parent_topic:: [[Topic - ML Training & MLOps]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[snorkel-team - snorkel]]]
- [related_to:: [[recipy - recipy]]]
- [mentions_term:: [[Glossary - Training Data Attribution]]]
- [mentions_term:: [[Glossary - Provenance]]]
- [mentions_term:: [[Glossary - LLM]]]

## Evidence
- Source URL: https://github.com/HCAI-Lab-GT/capabilibara
- Source kind: GitHub REST metadata plus the repository tree and files, read directly
- Ingestion mode: agent-curated note authored against a blobless shallow clone; no fetched code was executed
- Metadata captured: 2026-09-03
- Depth of read: recorded per source in [[Scouting Working File 2026-09-03]]

## GitHub Snapshot

- Description: Training-data attribution as a discovery method for capability provenance in language models. COLM 2026.
- Language: JavaScript
- License (SPDX): AGPL-3.0
- Default Branch: main
- Stars: 7
- Homepage: https://hcai-lab-gt.github.io/capabilibara/
- Pushed At: 2026-08-23T03:31:21Z
- Topics: ai-research, capability-provenance, interpretability, language-models, machine-unlearning, mechanistic-interpretability, research, training-data-attribution

## Evidence Anchors
- [github_repo] description :: Training-data attribution as a discovery method for capability provenance in language models. COLM 2026. (confidence 0.95)
- [github_repo] language :: JavaScript (confidence 0.90)
- [github_repo] license :: AGPL-3.0 (confidence 0.90)
- [github_repo] topics :: ai-research, capability-provenance, interpretability, language-models, machine-unlearning, mechanistic-interpretability, research, training-data-attribution (confidence 0.85)
- [repository_tree] structure read from a depth-1 blobless clone on 2026-09-03 (confidence 0.95)
