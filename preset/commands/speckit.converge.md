---
description: "Assess current code, test assertions, and verification evidence against the feature's spec, plan, and tasks; append only deduplicated remediation tasks to tasks.md."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile. Where a stock step below says something different, these rules win.

### Assess evidence, not only code

- Read `verification.md` alongside the spec, plan, tasks, and current code. Trace every FR and AS through its TR to an executable test or specified observation. Read the assertions; matching names, markers, matrix rows, or checkbox counts are not coverage.
- Assess the real interface where each promise is made. An isolated service test cannot certify a request, form, CLI, browser, or device workflow.
- Audit previously completed tasks and tests by the same standard. Required evidence that is missing, stale, skipped, failed, NOT RUN, or BLOCKED is a gap.
- Evidence is current only when it identifies the code and acceptance artifacts being assessed. Do not infer PASS from code inspection, an old log, or an earlier chat message. Identifying the assessed state (commit plus relevant working-tree fingerprint) is allowed; the stock "no git" rule means converge does not diff branches or history to find gaps.
- Audit reuse explicitly: duplicated authorization, validation, domain invariants, configuration, fixtures, and UI styling or interaction. An ignored suitable abstraction is a gap.
- Required commands and evidence must be runnable and retained locally. External hosting, review, automation, synchronization, work-item, or artifact-upload services cannot gate convergence. Historical external results are evidence only for the state they tested.

### Write limit

- This command may inspect existing results and run safe relevant tests. Its **only file write is appending to `tasks.md`**. Do not modify application code, the spec, the plan, existing tasks, `verification.md`, or any report file.
- If the spec or plan must change to add missing intent or mappings, recommend the specify or plan command. Do not edit them here and do not invent intent.
- Return the assessed-state fingerprint, findings, and outcome in the response. The enclosing implement/verify workflow records that outcome in `verification.md` after this command returns.

### Appending

- Do not append work that an open task already covers; cite that task's ID. A repeated run with unchanged gaps appends nothing.
- When a checked task's claim is unsupported, append a new remediation task and leave the old checkbox as history.
- Each appended task names its FR/AS/TR, affected paths, the verification expected after repair, and its dependencies.

### Outcomes

Report exactly one. This replaces the two-outcome wording in the stock "Append Convergence Tasks", "Provide Next Actions", and closing hook steps.

- `tasks_appended`: new uncovered remediation was appended, whether or not other existing gaps remain. Hand off to implement.
- `gaps_remaining`: nothing new needed appending, but open tasks, decisions, blockers, or missing/stale evidence remain. Leave `tasks.md` unchanged, cite the open task IDs and missing evidence, report NOT DONE, and hand off to implement.
- `converged`: no gaps remain **and** all required current verification passes. Leave `tasks.md` unchanged. Recommend review and a coherent commit under the project's version-control rules.

No new tasks is not the same as converged.

{CORE_TEMPLATE}
