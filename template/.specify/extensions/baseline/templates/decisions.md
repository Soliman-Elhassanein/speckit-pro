# Decisions: [PRODUCT NAME]

**Version**: 0.1.0 | **Last amended**: [YYYY-MM-DD]

This file says WHY. One row per decision, product or architecture, including the options that
were rejected. Rows are never deleted or rewritten: a changed decision gets a new row, and the
old row's status becomes `superseded by D-NNN`.
Only the baseline amend command edits this file, and only after the user approves the change.

**Status** is one of `accepted`, `rejected`, or `superseded by D-NNN`. **Affects** names the
parts, folders or globs the decision governs, comma separated, or `-` for a product decision.
It is how the right decisions are loaded for the code a plan will touch.

| ID | Date | Question | Decision | Rejected options | Affects | Status |
|----|------|----------|----------|------------------|---------|--------|
| D-001 | [YYYY-MM-DD] | [What had to be decided.] | [What was chosen, and the reason in one clause.] | [Options not taken.] | - | accepted |
