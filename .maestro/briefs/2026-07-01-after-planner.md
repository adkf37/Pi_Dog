# Checkpoint Brief - after-planner

Project: Pi_Dog
Checkpoint: after-planner
Return Phase: task-review
Generated: 2026-07-01

## What Happened Since The Last Checkpoint

- **Planner phase completed** — `backlog/README.md`, `backlog/phases.md`, `backlog/data_sources.md`, 10 task files, and `.maestro/agent_plan.md` created.
- **Project structure defined** — 6 phases scoped (scaffold → LLM → hardware → voice → sensors → demo), with `local_llm` profile and no cloud dependencies.
- **5 key decisions logged** in `.maestro/decisions.md`: agent slate (4 profiles), dual LLM backend (Ollama + llama.cpp), mock-first development, Pydantic-enum action vocabulary, and bench mode safety default.
- **No code written yet** — `src/` directory does not exist; repo contains only planning artifacts, `.gitignore`, `requirements.txt`, and `project_overview.md`.
- **No human feedback received** — `FEEDBACK.md` is empty; no guidance on scope priorities or hardware availability.

## What Will Be Spent Next

- **Task Review** (next phase, 1 agent session): tighten backlog tasks, surface risks, produce ordered execution plan, and confirm agent dispatch order. Expected ~50-100 tokens of plan delta.
- **Phase 0 — Scaffolding** (~3-5 build sessions): package scaffold, config, schema, policy, mock robot, and tests. All tasks are `pending` with `build` profile.
- **Phase 1 — LLM Integration** (~2-3 build sessions): Ollama client, llama.cpp client, planner, CLI demo.
- **Phase 2-4** (~3-6 build sessions): hardware bridge, voice loop, sensor reactions (contingent on priorities).
- **Phase 5 — Demo & Polish** (~1-2 validate + scribe sessions): one-command demo, benchmarks, docs.

## Questions

### Q1 — Phase 0 task ordering: batch or sequential?
The planner defined tasks 01-05 (scaffold → config → schema → policy → mock robot) with sequential dependencies. These could be batched into a single build session (one agent implements all five in one pass) or run as separate sessions per task.

**Question:** Should the first build agent attempt all Phase 0 tasks in one session, or dispatch one session per task?
**Options:** Batch all Phase 0 in one session; One session per task (01 then 02 then ...); 01-02 in first session, 03-04-05 in second
**Default:** Batch all Phase 0 in one session
**Decision:** default

### Q2 — LLM backend priority for v1 demo
Decision 002 calls for both Ollama and llama.cpp backends via `LLMBase`. The default is Ollama. Implementing both upfront doubles LLM integration effort.

**Question:** Should the build agent implement both backends during Phase 1, or ship with Ollama-only and add llama.cpp as a follow-up?
**Options:** Both backends in Phase 1; Ollama-only in Phase 1, llama.cpp deferred to Phase 5+; Ollama-only, drop llama.cpp entirely
**Default:** Both backends in Phase 1
**Decision:** default

### Q3 — Voice and sensor scope for v1
Phases 3 (voice loop) and 4 (sensor reactions) are stretch milestones. SunFounder's SDK exposes touch sensors and the speaker is optional. STT/TTS adds significant complexity.

**Question:** Should the initial build plan include voice and sensor phases, or defer them to a v2?
**Options:** Include all phases through sensor reactions in v1; Ship v1 after hardware bridge (Phase 2), defer voice/sensors; Ship v1 after LLM integration (Phase 1), defer everything hardware-related
**Default:** Ship v1 after hardware bridge (Phase 2), defer voice/sensors
**Decision:** default
