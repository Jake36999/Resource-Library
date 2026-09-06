---
uuid: "e8e6bd3f-f5c9-53c3-adbf-da1267734811"
canonical_url: "https://github.com/awslabs/awsome-distributed-ai"
repo_key: "awslabs/awsome-distributed-ai"
owner: "awslabs"
repo_name: "awsome-distributed-ai"
aliases: ["awslabs/awsome-distributed-ai", "https://github.com/awslabs/awsome-distributed-ai"]
type: "ai_resource"
primary_topic: "Agentic AI & Models"
secondary_topics: ["Infrastructure & Observability", "Architecture & Developer Playbooks"]
ecosystem: "Shell"
domain_primary: "Agentic_AI"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "Procedural"
patterns: ["Agent Orchestration", "Model Inference Pipeline"]
glossary_terms: ["Agent", "Inference", "Cloud", "LLM", "Prompt", "TTS", "STT", "Multimodal Model"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 6
github_description: "Collection of best practices, reference architectures, model training examples and utilities to train large models on AWS. "
github_language: "Shell"
github_license: "Unknown"
github_license_spdx: "MIT-0"
github_default_branch: "main"
github_stars: 0
github_topics: ["aws", "distributed-inference", "distributed-training", "efa", "eks", "generative-ai", "gpu", "hyperpod", "kubernetes", "parallelcluster", "physical-ai", "slurm"]
github_homepage: "https://awslabs.github.io/awsome-distributed-ai/"
github_pushed_at: "2026-09-04T11:49:18Z"
github_updated_at: "2026-08-31T13:08:19Z"
---

# awslabs - awsome-distributed-ai

## Bottom Line
Reference architectures and runnable examples for distributed AI training and inference on AWS — SageMaker HyperPod, ParallelCluster, PCS and EKS — including cluster templates, custom machine images, health validation and benchmarks.

## What It Solves
- Get a working distributed training cluster without assembling the infrastructure from scratch.
- Validate that a cluster is healthy before committing an expensive training run to it.
- Compare training approaches across several AWS orchestration services.

## Architecture & Mechanics
- `architectures/` holds cluster deployment templates for each supported service.
- `ami/` contains scripts for building custom machine images.
- `examples/` provides runnable training and inference demonstrations grouped by framework.
- `validation/` offers health checks and `observability/` monitoring and profiling; `micro-benchmarks/` tests network and GPU performance.

## What Is Inside
- **Not a list — 1,454 files of runnable infrastructure.** The name misleads: `examples/` (648) and `architectures/` (401) contain deployable stacks, not links.
- **Reference architectures per platform** — `architectures/`: `sagemaker-hyperpod-eks` (200), `sagemaker-hyperpod-slurm` (127), `aws-pcs` (43), `aws-parallelcluster` (12), `amazon-eks` (8), `vpc_network`, `accounting-database`. 97 `.tf` files and 105 IaC paths overall.
- **Training and inference examples that run** — `examples/training/` (370, including `torchtitan/slurm/configs/llama3_8b.toml` and an FP8 variant), `examples/inference/` (90, with NVIDIA Dynamo and SGLang deployments), `examples/use-cases/` (188). 68 `.sbatch` Slurm job scripts.
- **A micro-benchmark suite for interconnects** — `micro-benchmarks/`: `expert-parallelism` (64), `nccl-tests` (19), `nvshmem` (5), `nccl-sendrecv` (4), `nccom-tests` (3). This is how you measure a cluster before trusting it.
- **Observability stacks ready to deploy** — `observability/`: `prometheus-grafana` (51), `nsight` (32), `efa-node-exporter` (28), with DCGM GPU metric definitions as CSV (`dcgm-metrics-basic.csv`, `dcgm-metrics-advanced.csv`).
- **Regression testing of the examples themselves** — `.github/workflows/fsdp-regression-test-container.yml` and a Slurm-backed PR review workflow.
- **Agent instructions at three levels** — `AGENTS.md`, `CLAUDE.md`, and `.opencode/skills/` with `SKILL.md` files for `bash-testing` and `build-slurm-image`.

## Transferable Capability
**Measure the substrate before trusting it, with the same tests everyone else runs.** For work whose cost is dominated by how well many machines communicate, a reference architecture is worth little without the measurements that show it performs — so the benchmarks ship beside the deployment. The separable practice: **regression-test the published examples themselves**, so an example that stops working is a build failure rather than somebody's afternoon. The same discipline extends to the contribution procedure itself, which is **shipped as executable skills** - build this image, test that script - rather than described in a guide nobody reads twice.

**Alternative to:** reference architectures published without measurement, and examples that rot silently. **Applies wherever** performance depends on an environment you assemble and the assembly can be wrong in ways that look fine.

## Taxonomy
- Ecosystem: Shell
- Domain Primary: Agentic_AI
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: Procedural

## Integration & Use Cases
- Stand up a distributed training cluster from a reference architecture.
- Health-check and benchmark GPU infrastructure before a long run.
- Study how large-scale training deployments are structured in practice.

## Semantic Links
- [parent_topic:: [[Topic - Agentic AI & Models]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[Azure-Samples - semantic-kernel-advanced-usage]]]
- [related_to:: [[vercel-labs - skills]]]
- [related_to:: [[armanakbari - Awsome-Efficient-DLMs]]]
- [implements_pattern:: [[Pattern - Agent Orchestration]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Agent]]]
- [mentions_term:: [[Glossary - Inference]]]
- [mentions_term:: [[Glossary - Cloud]]]
- [mentions_term:: [[Glossary - LLM]]]
- [mentions_term:: [[Glossary - Prompt]]]
- [mentions_term:: [[Glossary - TTS]]]
- [mentions_term:: [[Glossary - STT]]]
- [mentions_term:: [[Glossary - Multimodal Model]]]

## Evidence
- Source URL: https://github.com/awslabs/awsome-distributed-ai
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Collection of best practices, reference architectures, model training examples and utilities to train large models on AWS. 
- Language: Shell
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: https://awslabs.github.io/awsome-distributed-ai/
- Archived: no
- Disabled: no
- Pushed At: 2026-08-31T13:01:56Z
- Updated At: 2026-08-31T13:08:19Z
- Topics: aws, distributed-inference, distributed-training, efa, eks, generative-ai, gpu, hyperpod, kubernetes, parallelcluster, physical-ai, slurm

## Evidence Anchors
- [github_repo] description :: Collection of best practices, reference architectures, model training examples and utilities to train large models on AWS. (confidence 0.95)
- [github_repo] topics :: aws, distributed-inference, distributed-training, efa, eks, generative-ai, gpu, hyperpod, kubernetes, parallelcluster, physical-ai, slurm (confidence 0.82)
- [github_repo] language :: Shell (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
