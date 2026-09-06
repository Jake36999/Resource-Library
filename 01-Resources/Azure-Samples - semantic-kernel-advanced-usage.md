---
uuid: "6067ee76-414a-5dc5-acaf-8ba89807f734"
canonical_url: "https://github.com/Azure-Samples/semantic-kernel-advanced-usage"
repo_key: "Azure-Samples/semantic-kernel-advanced-usage"
owner: "Azure-Samples"
repo_name: "semantic-kernel-advanced-usage"
aliases: ["Azure-Samples/semantic-kernel-advanced-usage", "https://github.com/Azure-Samples/semantic-kernel-advanced-usage"]
type: "ai_resource"
primary_topic: "Agentic AI & Models"
secondary_topics: ["Architecture & Developer Playbooks"]
ecosystem: "Python"
domain_primary: "Agentic_AI"
maturity_stage: "Active"
license_class: "Permissive"
deployment_target: "Local_Only"
interface_protocol: "Python_SDK"
data_locality: "Local_First"
hardware_footprint: "Low_VRAM"
security_compliance: "Uncertified"
agent_surface: "Callable"
patterns: ["Agent Orchestration", "Model Inference Pipeline"]
glossary_terms: ["Agent", "LLM", "Prompt", "Inference", "TTS", "STT", "Multimodal Model"]
status: "published"
maturity: "curated"
evidence_refreshed: "2026-09-01"
sensitivity: "normal"
license: "MIT"
source_file: "repositories to chart.md"
evidence_count: 5
github_description: "Collection of advanced usage scenarios for Semantic Kernel"
github_language: "Python"
github_license: "Unknown"
github_license_spdx: "MIT"
github_default_branch: "main"
github_stars: 0
github_topics: []
github_homepage: ""
github_pushed_at: "2026-04-21T20:36:03Z"
github_updated_at: "2026-08-01T12:35:32Z"
---

# Azure-Samples - semantic-kernel-advanced-usage

## Bottom Line
Eight self-contained reference scenarios for Microsoft's Semantic Kernel, covering the patterns its own documentation does not — orchestration, Dapr hosting, process frameworks and tracing — each runnable independently.

## What It Solves
- Bridge the gap between Semantic Kernel's introductory documentation and production usage.
- Show orchestration and hosting patterns as working code rather than description.
- Provide starting points for problems such as natural-language-to-SQL and multi-agent coordination.

## Architecture & Mechanics
- Eight scenario folders, each self-contained with its own requirements file.
- Scenarios include natural language to SQL, multi-agent speaker selection and Copilot Studio integration.
- Dapr hosting and process-framework examples cover deployment rather than just invocation.
- Tracing examples address observability of agent runs. Maintained by Azure-Samples under MIT.

## What Is Inside
- **Nine self-contained templates, not a library** — `templates/` is 209 of the repository's 224 files, each subdirectory a working pattern rather than a snippet: `advanced_orchestration_dapr/` (51 files, multi-agent orchestration over Dapr, with per-service dockerfiles and a chat front end), `copilot-agent-ms-graph/` (40, an agent against Microsoft Graph), `natural_language_to_SQL/` (31, shipping a `healthcare_data.db` SQLite file to query against), `copilot_studio_skill/` (28), `authentication_context/` (20, on-behalf-of auth flows), `sk_mcp/` (9, a Semantic Kernel MCP server with vendored `mcp_docs/llms-full.txt`), `speaker_selection_strategy/` (12), `opentelemetry/`.
- **Runnable notebooks** — `templates/speaker_selection_strategy/playground.ipynb`, `templates/opentelemetry/play.ipynb`, `templates/copilot_studio/src/test.ipynb`, `templates/advanced_orchestration_dapr/src/agents/tests/test_team.ipynb`.
- **Azure infrastructure as code** — 20 `.bicep` files across the templates, plus `azure.yaml` and `dapr.yaml` deployment descriptors; 14 `.env.sample` files documenting the settings each pattern needs.
- **What to reach for it for:** the orchestration and speaker-selection templates are the reusable part. There is no importable package — you copy a template.

## Transferable Capability
**Publish complete working arrangements rather than fragments, because the hard part is how the pieces fit and a fragment omits exactly that.** Each unit deploys, so the assumptions are visible in configuration and infrastructure rather than left as a reader's exercise. The cost is that nothing composes — you copy an arrangement, you do not import it.

**Alternative to:** documentation showing the interesting call and eliding the setup, where the reader rediscovers the integration problem. **Applies wherever** the difficulty is in assembly rather than in any individual part.

## Taxonomy
- Ecosystem: Python
- Domain Primary: Agentic_AI
- Maturity Stage: Active
- License Class: Permissive
- Deployment Target: Local_Only
- Interface Protocol: Python_SDK
- Data Locality: Local_First
- Hardware Footprint: Low_VRAM
- Security Compliance: Uncertified
- Agent Surface: Callable

## Integration & Use Cases
- Adopt a Semantic Kernel orchestration pattern from working code.
- Study multi-agent coordination as implemented rather than described.
- Reference tracing approaches for agent workflows.

## Semantic Links
- [parent_topic:: [[Topic - Agentic AI & Models]]]
- [taxonomy_hub:: [[Taxonomy Index]]]
- [related_to:: [[vercel-labs - skills]]]
- [related_to:: [[awslabs - awsome-distributed-ai]]]
- [related_to:: [[armanakbari - Awsome-Efficient-DLMs]]]
- [implements_pattern:: [[Pattern - Agent Orchestration]]]
- [implements_pattern:: [[Pattern - Model Inference Pipeline]]]
- [mentions_term:: [[Glossary - Agent]]]
- [mentions_term:: [[Glossary - LLM]]]
- [mentions_term:: [[Glossary - Prompt]]]
- [mentions_term:: [[Glossary - Inference]]]
- [mentions_term:: [[Glossary - TTS]]]
- [mentions_term:: [[Glossary - STT]]]
- [mentions_term:: [[Glossary - Multimodal Model]]]

## Evidence
- Source URL: https://github.com/Azure-Samples/semantic-kernel-advanced-usage
- Source kind: project documentation fetched from the source repository
- Ingestion mode: rewritten from fetched evidence, replacing the topic-template bootstrap
- Evidence refreshed: 2026-09-01
- Licence resolved from the LICENSE on 2026-09-03: LICENSE names MIT (reproduced in full). The GitHub API reported `UNKNOWN`, which is why this was read directly.

## GitHub Snapshot

- Description: Collection of advanced usage scenarios for Semantic Kernel
- Language: Python
- License: Unknown (UNKNOWN)
- Default Branch: main
- Stars: 0
- Watchers: 0
- Homepage: None provided
- Archived: no
- Disabled: no
- Pushed At: 2026-04-21T20:36:03Z
- Updated At: 2026-08-01T12:35:32Z
- Topics: None provided

## Evidence Anchors
- [github_repo] description :: Collection of advanced usage scenarios for Semantic Kernel (confidence 0.95)
- [github_repo] language :: Python (confidence 0.74)
- [github_repo] license :: Unknown (UNKNOWN) (confidence 0.90)
- [seed] repositories to chart.md :: - [ ] https://github.com/Azure-Samples/semantic-kernel-advanced-usage.git (confidence 0.50)
