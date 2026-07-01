# Copilot Coding Agent - Maestro Project Instructions

<!-- Managed by Maestro workflow contract. Update `workflow_contract.yaml` instead of editing this file directly. -->

This project is managed by the **Maestro** orchestration system and uses provider-neutral Maestro agent profiles for coordination.

## Before Starting Work

1. `STATUS.md` - current phase, machine-readable `Next Action`, objective, blockers, and next recommended step
2. `FEEDBACK.md` - human corrections or guidance, if present

If these files or directories exist, read them next:

- `backlog/README.md` - project goals and success criteria
- `backlog/data_sources.md` - known data sources and constraints
- `backlog/tasks/` - discrete task definitions
- `.maestro/agent_plan.md` - repo-local Maestro agent routing plan, if present
- `.maestro/task_plan.md` - repo-local execution plan, if present
- `.maestro/memory.md` - curated project fact sheet, constraints, conventions, and dead ends, if present
- `.maestro/decisions.md` - repo-local decision log, if present

## Work Conventions

- **Branch naming:** `maestro/{phase}-{kebab-case-slug}`
- **Commit messages:** Use one of these phase prefixes: `[Planner]`, `[Task Review]`, `[Build]`, `[Brief]`, `[Critic]`, `[Validate]`, `[Closeout]`
- **Status updates:** Update `STATUS.md` whenever you change the phase, objective, blockers, or next step. Keep a machine-readable `Next Action` field set to `Task Review`, `Build`, `Validate`, `Closeout`, `Complete`, or `Human Blocked`. Use `Complete` only when every planned task is complete.
- **Decisions:** Log significant architectural, data, and validation decisions in `.maestro/decisions.md`.

## Phases

This repo follows the Maestro lifecycle:
1. **Planner** - Survey the existing repo, define the deliverable, create the backlog contract, and select the project agent slate.
2. **Task Review** - Tighten backlog tasks, surface risks, and turn the backlog into an execution plan.
3. **Build** - Execute one or more independent implementation or analysis tasks from the plan in a single session.
4. **Checkpoint Brief** - Prepare a one-page human decision brief at a configured checkpoint without blocking project autonomy.
5. **Adversarial Critic** - Red-team the cumulative deliverable against acceptance criteria, methodology, claims, and runnability.
6. **Validate** - Run the right checks, capture evidence, and decide whether the loop advances or returns to build.
7. **Closeout** - Refresh handoff artifacts and decide whether the project is complete, human-blocked, or returns to one explicit task.

Legacy aliases still appear in older repos:

- `coder` maps to `build`
- `reviewer` maps to `closeout`
- `review` maps to `closeout`

## Artifact Contract

### Planner

- `backlog/README.md` - project background, goals, and success criteria
- `backlog/data_sources.md` - source URLs/endpoints and availability status
- `backlog/phases.md` - lifecycle breakdown aligned to Maestro phases
- `backlog/tasks/` - one file per discrete task
- `.maestro/agent_plan.md` - repo-local agent slate, responsibilities, routing rules, and handoff expectations
- `.maestro/decisions.md` - decision log initialized if absent
- `.maestro/memory.md` - curated fact sheet initialized if useful
- `STATUS.md` - current objective updated to reflect the plan
- `requirements.txt` - created or updated if additional Python packages are needed

### Task Review

- `backlog/tasks/` - detailed, fully specified task files
- `.maestro/task_plan.md` - ordered execution plan with task IDs, recommended agent profile, dependencies, and status
- `STATUS.md` - updated to show review is complete and the repo is ready for `build`

### Build

- Implementation work that materially advances one or more explicit tasks from `backlog/tasks/` or dated `FEEDBACK.md` items; each task cited by its ID
- `STATUS.md` - updated with progress, blockers, all task/feedback IDs worked, and machine-readable `Next Action`
- `.maestro/decisions.md` - significant implementation decisions and task/feedback IDs
- `.maestro/memory.md` - update only for durable facts, constraints, conventions, or dead ends discovered during the work

### Checkpoint Brief

- `.maestro/briefs/<date>-<checkpoint>.md` - one-page decision brief with questions, options, defaults, and machine-readable `Decision:` lines
- `STATUS.md` - left on its prior `Next Action`; do not set `Human Blocked` from a brief

### Adversarial Critic

- `.maestro/critic_report.md` - adversarial review, commands run, evidence checked, findings, and final verdict
- `FEEDBACK.md` - structured entries for each critic finding with `Scope: critic`, `Severity: block|warn`, `Status`, and linked task IDs where possible

### Validate

- Tests, lint, type checks, metrics, evals, or data integrity checks run when applicable
- `.maestro/validation_report.md` - commands/checks run, results, blocked checks, evidence, and pass/fail recommendation
- `STATUS.md` - updated with pass/fail/blocked outcome and next recommended phase
- `.maestro/decisions.md` - validation evidence and rationale
- `.maestro/memory.md` - update only for durable validation lessons or environment constraints

### Closeout

- `STATUS.md` - updated with closeout outcome, remaining blockers, and machine-readable `Next Action`
- `.maestro/review_report.md` - final decision, evidence checked, risks, and explicit `Complete` only when every planned task is complete, `Human Blocked`, or return-to-build decision with task/feedback ID
- `.maestro/decisions.md` - final closeout decisions, handoff notes, and task/feedback ID if returning to build
- `.maestro/memory.md` - curated, capped to roughly 100 lines; prune stale details and keep only durable facts, constraints, conventions, and dead ends
- Human-facing docs refreshed enough for handoff

## Data Constraints

- Prefer using data already in the repo (`data/`, `cache/`, CSV files) when possible.
- If external data is needed, document the source URL in the backlog and any dependency changes in `requirements.txt`.
- Never hardcode API keys - use environment variables.
