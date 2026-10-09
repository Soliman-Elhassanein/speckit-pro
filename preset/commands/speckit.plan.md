---
description: "Plan the feature with a reuse inventory, a verification plan, exact quality gates, and a verification record that starts as NOT RUN."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (sections 4.2, 5.5, 6 and 7). Where a stock step below says something different, these rules win.

### Design

- Run the Constitution Check before the design and again after it.
- Fill "Reuse inventory" before proposing new code: search the repository for helpers, services, components, validators, fixtures and utilities that already do the job. Each shared rule or data shape gets one authoritative home. Explain any duplication you keep on purpose.

### Verification

- Fill "Verification plan": one row per TR in the spec, at the smallest layer that can prove it, including the real interface where the promise is made. Name the test file, the selector or command, and the prerequisites and fixtures.
- Fill "Quality gates" with the exact commands and working directories the repository already uses. Do not add a tool because you prefer it.
- If `FEATURE_DIR/verification.md` does not exist, create it from the `verification-template`:

  ```sh
  .specify/scripts/bash/resolve-template.sh verification-template
  ```

  Fill in the IDs and planned selectors, and leave every status `NOT RUN`. If the file exists, keep its recorded runs and add only the missing rows.

### Project baseline

- When a hook before this command handed over a block that starts with `**Architecture impact**:`, write that block directly below the `**Input**` line, unchanged.

{CORE_TEMPLATE}
