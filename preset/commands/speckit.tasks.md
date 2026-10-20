---
description: "Keep safe parallel markers and two change-size paths."
strategy: wrap
---

## speckit-pro rules

- Full path for features: specify → clarify → plan → tasks → analyze → implement →
  converge. Light path for small changes and bug fixes: name approved behavior and
  what must stay unchanged, reproduce bugs with a failing test where applicable,
  make the change and run applicable gates. Do not manufacture feature artifacts
  for the light path; neither path may change memory meaning without amend approval.
- `[P]` only on tasks that touch different files and no shared state within the
  same phase. If independence is uncertain, leave the marker off.
- Behavior tests are required even where upstream marks them optional. Include
  behavior tests before implementation and trace tasks to existing spec
  requirements. Keep IDs, existing text, order and checked boxes; append new work
  above the maximum ID. Replace closing-phase markers with real sequential IDs and
  an ascending `## Phase N: Verification and convergence` heading.

{CORE_TEMPLATE}
