---
description: "Check Focus scope and consistency without changing files."
strategy: wrap
---

## speckit-pro rules

- Stay read-only. Compare spec, plan and tasks with cited product promises,
  capabilities, accepted decisions, architecture rules and part boundaries.
- Scope check: plan and tasks must not grow beyond what the `## Focus` section
  justified. Report each unjustified addition with its location and recommend
  reducing scope or obtaining an approved amendment; do not invent approval.
- Report missing requirement coverage, contradictions and violations of blocking
  Delivery standards.
- Report every `[P]` task that depends on another task of its phase, and every phase
  whose end state cannot pass the plan's Quality gates (for example a gate on a folder
  the phase leaves empty). Scripts validate references; judge meaning here with the user.

{CORE_TEMPLATE}
