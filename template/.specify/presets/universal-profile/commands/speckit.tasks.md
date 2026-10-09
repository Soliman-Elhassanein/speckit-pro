---
description: "Generate dependency-ordered tasks with mandatory tests, traceable verification work, and a closing verification and convergence phase."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (sections 4.2, 5.6 and 6.2). Where a stock step or the tasks template below says something different, these rules win.

- **Tests are mandatory.** Ignore every "OPTIONAL" and "only if requested" note about tests in the template.
- Order the work inside each story: acceptance and behavior tests, supporting tests, implementation, focused verification and repair, related regressions.
- Every test and verification task names the FR, AS and TR it covers and the test path or selector from the plan's "Verification plan". Every FR and AS in the spec maps through a TR to at least one task.
- Add a task for each reuse or extraction the plan's "Reuse inventory" calls for.
- Keep the template's closing phase, "Verification and convergence", as the last phase, with real task IDs.
- Mark a task `[P]` only when it shares no file, state, service, device or other resource with the tasks it would run beside.
- When `tasks.md` already exists, keep its IDs, checked boxes and order, and append new tasks above the current maximum ID.

{CORE_TEMPLATE}
