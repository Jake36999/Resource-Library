---
type: "application_record"
project: "AI systems - agent harnesses, fine-tuning and training pipelines"
stage: "ongoing capability development"
date_range: "2024 - ongoing"
status: "active"
resources_used: ["agent harness implementations", "training and fine-tuning pipeline repositories", "model implementations across modalities"]
patterns_discovered: ["a context problem is often a documentation problem", "capability compounds faster than expected"]
domains: ["agentic_ai_models", "ml_training_mlops", "signal_audio_speech"]
outcome: "progressed from prompt engineering to building harnesses and pipelines; next targets are a semantic fine-tuning pipeline and training a model from scratch"
---

# Application - Agent Harnesses And Training Pipelines

## What Was Needed
A ramp rather than a single problem. Two years ago building custom agent harnesses and training pipelines looked like a lifetime's distance away. The route ran through advanced multi-step YAML system prompts with Python integration, using services' own systems to get more out of their models — and from there into building the surrounding machinery.

## What Was Found And Taken
Existing harness implementations and pipeline repositories, used mostly for **structure**: how the pieces are separated, where state lives, what a training pipeline actually consists of once it stops being a script. The value of open source here is less about the code and more about seeing a working decomposition of a problem you have not solved before.

More recently the search has broadened across model types — sensing models, TTS and STT, emulation models — where the question is what each kind of model requires structurally rather than which specific one to use.

## What It Replaced
The alternative was inventing an architecture for each piece with no reference for what a good one looks like — slow, and likely to produce something that works but does not extend.

## Patterns And Insights
**A context problem is often a documentation problem.** At one point the projects seemed to require more advanced reasoning over large context. They did not. The real issue was that the documentation system and workflows were immature, so the model was being asked to reconstruct context that should simply have been recorded. This is worth stating plainly because the instinct — reach for a bigger model or a longer context window — is expensive and wrong. This catalogue is in part a response to that finding.

**Capability compounds faster than the estimate.** The distance from prompt engineering to building training pipelines looked like years and was not. Worth remembering when scoping the next thing that looks out of reach.

## Current And Intended Directions
- Maturing the semantic agent fine-tuning pipeline.
- Training a model from scratch, resources permitting.
- Models that orchestrate games.
- Optimisation methods, and optimised models running on lightweight hardware for specific applications.
- A low-gain trading bot.

Each of these is a distinct search with distinct vocabulary, which is the point for the catalogue.

## What The Catalogue Should Learn
1. **Hardware footprint is a primary filter for this work, not a secondary one.** Anything targeting lightweight hardware needs quantisation, distillation and efficient-inference material findable by constraint. The axis exists; it is not yet used as a filter.
2. **The directions above name domains the register does not cover.** Model training and MLOps is already tier 1. Game-orchestrating models, emulation models, and quantitative or trading systems are not covered at all.
3. **Prefer resources with a working decomposition over resources with good features.** What repeatedly helped here was seeing how a problem was carved up. Nothing currently records that, and the `depth` ranking signal is the closest proxy.

## Semantic Links
- [application_hub:: [[Application Index]]]
- [related_topic:: [[Topic - Agentic AI & Models]]]
- [related_workflow:: [[Workflow - Adopt A Dependency]]]
