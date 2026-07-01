# Agent Plan — PiDog Local LLM Brain

## Agent Slate

| Profile | Responsibility | Tasks |
|---------|---------------|-------|
| planner | Scope, decompose, define dependencies, plan artifacts | (current phase) |
| build | Implementation: Python package, LLM client, robot adapter, CLI | task-01 through task-10 |
| validator | Run pytest, lint, type checks; validate against acceptance criteria | task-review / validate phases |
| scribe | Documentation: README, hardware setup, model benchmarks, demo plan | cross-cutting |

## Routing Rules

- **Backlog creation / refinement** → planner
- **Python implementation** → build
- **Docs-only changes** → scribe
- **Test/validation runs** → validator
- **PR review / acceptance check** → validator
- **Closeout / handoff** → scribe

## Handoff Expectations

- build hands off to validator with task IDs, test evidence, and any decisions made.
- validator hands off to scribe with pass/fail/blocked outcome.
- scribe hands off to next phase with refreshed docs and STATUS.md.

## Agent Selection Rationale

Minimal slate for a `local_llm` project: planner + build + validator + scribe.
No critic required until closeout. No separate MLE or data engineer needed — all data sources are public SDK docs.
