---
description: "Implement the tasks test-first, then verify on the final state, record the evidence in verification.md, and converge."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (sections 5.8, 6.2, 7 and 8). Where a stock step below says something different, these rules win.

### While implementing

- Read the spec, the plan, the tasks and `verification.md` together. Run the existing gates once before changing behavior, and record what was already failing.
- Follow test, expected failure, implement, run, diagnose, fix, rerun. A missing device, credential, service or broken harness is `BLOCKED`. It is not an expected failure and it is not a pass.
- Never weaken, delete, skip or disable a valid check to get a pass, and never change approved behavior to satisfy a test.
- Check a task only when its own validation passes.

### Verify

After the last task, on the final state of the code:

1. Run every command under "Quality gates" in `plan.md`, complete, not a subset.
2. Record the run in `FEATURE_DIR/verification.md`. If the file is missing, create it from the `verification-template` (`.specify/scripts/bash/resolve-template.sh verification-template`). Record the tested state, each exact command with its working directory, exit code and counts, and the status of every TR row.
3. Use only `PASS`, `FAIL`, `NOT RUN` and `BLOCKED`. Claim `PASS` only from a finished process with its exit status. Move a superseded run under "Historical runs" with its original status; do not relabel it.

### Converge and complete

1. Run the converge command. Tasks that a review appended before it are open work like any other.
2. Write its outcome on the `Outcome:` line of the "Convergence" section, with the assessment date and the assessed state.
3. On `tasks_appended` or `gaps_remaining`, do the open work, verify again and converge again. Stop honestly when the work is blocked or outside what was authorized.
4. Set `Completion: DONE` only when every status is `PASS`, every coverage count is complete, every task is checked, and the outcome is `converged`. Otherwise it stays `NOT DONE`.
5. When `.specify/extensions/baseline/scripts/baseline_check.py` exists, run it. It rejects a `DONE` that the record does not support: a missing plan or tasks file, an unchecked task, a requirement ID without a passing Coverage row, a non-zero exit code, a failure count, an unresolved evidence link, or an outcome other than `converged`. Fix the record or the work; never reword the record to get past the check.

{CORE_TEMPLATE}
