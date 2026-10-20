---
description: "Write concrete Quality gates and retain the approved scope."
strategy: wrap
---

## speckit-pro rules

- Retain context's `**Architecture impact**`, `**Parts**`, `**Architecture rules**`
  and `**Decisions**` citation lines. Keep the design within the spec's Focus scope.
- Complete exactly `## Quality gates` with columns `Gate`, `Command`: one concrete
  command per row in a single code span, runnable from the repository root. No
  placeholders. Use the project's existing checks.
- Automatically add every applicable decided Delivery standards row with a Check
  command as a gates row. Resolve touched undecided areas through baseline.amend;
  blocking Delivery rows are non-negotiable. Do not silently omit a decided check.
- Create verification.md from verification-template if absent; seed planned commands
  with NOT RUN exits, retain existing results honestly, and leave Completion NOT DONE.

{CORE_TEMPLATE}
