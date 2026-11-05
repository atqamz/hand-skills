---
name: hand-commit-message
description: Write a commit message that follows Hand's rules. Use when an agent in a Hand fleet is about to commit or amend a commit.
---

# Commit message

1. Stage one self-contained change. Split unrelated work into separate commits.
2. Write the subject in the imperative mood, lowercase first word, no trailing period, at most 72 characters.
3. State the change, not the plan. Do not use the words phase, step or milestone.
4. Add a body only for what the diff cannot show: why, a measurement, an external constraint, a failure mode.
5. Add no attribution lines: no `Co-Authored-By`, no "Generated with".
6. Commit only when the operator or the task brief authorizes it. Never skip hooks or signing.

Good: `fix wake loop when a report arrives twice`

Bad: `Phase 2: Fixed the wake loop.`

## Needs

Nothing.
