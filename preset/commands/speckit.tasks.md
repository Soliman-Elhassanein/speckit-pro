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
- `[P]` only on tasks that touch different files, share no state and depend on no
  other task in the same phase. A task that must wait for another one ("after T003
  fails") is never `[P]` beside it: put the test and its implementation in order
  without the marker, or in consecutive phases. If independence is uncertain, leave
  the marker off.
- Each phase must end with every Quality gate passing on that phase's own result: a
  phase's failing tests and the code that makes them pass belong to the same phase,
  and Git keeps no empty folders, so a folder a gate needs must receive a file.
- Keep every task small: one behavior or one requirement, the few files it needs, and
  one check that proves it (a test or a gate). Split a task that changes several
  behaviors, screens or layers, or whose description joins separate changes with "and";
  a test task and the implementation it proves are separate tasks.
- Behavior tests are required even where upstream marks them optional. Include
  behavior tests before implementation and trace tasks to existing spec
  requirements. A task that writes a failing test saves that failing run's output
  to its own log file in the feature folder (for example `logs/T004-red.log`), so
  test-first evidence survives and `[P]` tasks never share a record.
- The closing phase only runs and records the Quality gates. Converge, its
  remediation and the DONE check follow the tasks and are never tasks: no task
  assesses readiness, appends tasks or ticks another task. Keep IDs, existing text, order and checked boxes; append new work
  above the maximum ID. Replace closing-phase markers with real sequential IDs and
  an ascending `## Phase N: Verification and convergence` heading.

{CORE_TEMPLATE}
