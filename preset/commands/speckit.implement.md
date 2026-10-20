---
description: "Implement test-first and retain gate results."
strategy: wrap
---

## speckit-pro rules

- Implement test-first: write a meaningful behavior test, observe the expected
  failure, implement, rerun and repair. Missing prerequisites are blockers, not
  expected failures. Never weaken valid checks or approved behavior to get a pass.
- Check tasks only after their validation and the phase gates pass on the combined
  code state. After implementation, run every Quality gates command from plan.md.
- Record exact gate commands, actual exit codes and local log paths in verification.md,
  plus remaining gaps. No executed command means NOT RUN; blocked or failed work
  cannot count as passing.
- Run converge and record its returned outcome. For tasks_appended or gaps_remaining,
  repair and verify again. Set Completion: DONE only with every task checked, every
  gate exited 0 and converged; run
  `python3 .specify/extensions/baseline/scripts/baseline_check.py --done --feature <feature folder>`.
- Let converge finish write-back, the feature commit and the delivery approval
  question; do not create a second commit or deliver independently.
- Follow the approved Git & branching Delivery rule. Default Conventional Commits:
  `<type>[optional scope]: <Description>`, blank line, optional body and footers.
  Types: feat, fix, refactor, perf, test, docs, style, build, ci, ops, chore, revert.
  Subject at most 50 characters; description capitalized, imperative, no trailing
  period. Body wrapped at 72 characters, explaining what changed and why.
  Footer `Refs: APP-142` or `Refs: 007` matches the branch id. Example:
  `feat: Add login rate limit`.

{CORE_TEMPLATE}
