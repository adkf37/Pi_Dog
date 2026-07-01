# FEEDBACK - Pi_Dog

> Drop feedback here for the next Maestro worker to pick up.
> The assigned agent reads this file at the start of each work cycle.
> Maestro parses this file: every entry with `Status: open` (or `in-progress`)
> blocks closeout from declaring `Complete` and is injected into the next
> dispatch prompt.

## Format

```
### YYYY-MM-DD - [Your Name or "Human"]
Status: open
Priority: [high | medium | low]
Scope: [direction | code | data | priority]
Linked Tasks: [task-12, task-15]  # optional

[Your feedback here]
```

Status values:
- `open` — not yet acted on (default if `Status:` omitted)
- `in-progress` — agent is working on it; still blocks Complete
- `addressed` — done; PR/commit reference in body
- `wontfix` — intentionally skipped; body must explain why

## Feedback Log

_(No feedback yet - project just activated.)_
