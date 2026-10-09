---
description: "Read-only analysis of spec, plan, tasks and evidence, with coverage by FR, AS, TR and task, and a check against the project baseline."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (sections 5.7 and 5.12). Where a stock step below says something different, these rules win. This command stays read-only: it writes no file.

### Coverage

- Report coverage separately for FRs, ASs, TRs and tasks. An FR or AS with no TR, a TR with no task, and a TR with no planned selector are each a gap.
- Read `verification.md` when it exists. Tell planned `NOT RUN` work apart from a completion claim that the evidence does not support.
- Judge the assertions and the interface they exercise, not ID matches. A test at the wrong layer does not cover a promise made at a request, form, CLI, browser or device.
- Report duplicated invariants, parallel components that do the same job, and reuse the plan ignored.

### Project baseline

Run this pass when `.specify/memory/product.md` exists. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`; when that script is not installed, read the baseline files directly.

1. Run `CHECK`. Report each error it prints as a CRITICAL finding, in its own words.
2. Load only what this feature cites and touches:

   ```sh
   CHECK --context --ids <every CAP, PR, AR and D ID in spec.md and plan.md>
   CHECK --context --paths <the folders and files plan.md and tasks.md name>
   ```

3. Compare, and record a finding only where the text shows the problem:

   | Compare | Finding when |
   |---------|--------------|
   | spec.md with its capabilities and the product rules | A requirement goes beyond, falls short of, or contradicts the capability's promise or a product rule. |
   | plan.md with the parts touched | The design reaches into a part that the "May depend on" cell does not allow, or keeps a second copy of something another part owns. |
   | plan.md with the architecture rules and decisions | The design breaks a rule, goes against an accepted decision, or uses a rejected option. |
   | plan.md's "Architecture impact" with the design | The label says `none` or `extends` and the design needs more. |
   | tasks.md with plan.md | A task creates or changes code in a folder that no part maps, or outside what the plan declared. |

4. Severity: CRITICAL when the finding contradicts an approved capability, a product rule, an architecture rule marked Blocking, or an accepted decision. HIGH for any other architecture rule or boundary.

For each finding, recommend one of: change the spec, plan or tasks, or amend the baseline through the baseline amend command. Do not choose for the user.

{CORE_TEMPLATE}
