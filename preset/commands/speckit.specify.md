---
description: "Create or update the feature specification with stable FR, AS, TR and SC identities and a verification matrix."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (sections 4, 5.3 and 6.1). Where a stock step below says something different, these rules win.

### Identity

- Give every acceptance scenario an ID, `AS-001` upward, unique across the whole feature and not per story. Keep the Given/When/Then wording after the ID.
- Give every test requirement an ID, `TR-001` upward. A TR states what must be observed to believe an FR or AS, not how it is coded.
- When the spec already exists, update it in place. Never renumber: keep existing IDs, suffixes and legacy aliases, and append new ones above the current maximum.

### Verification

- Fill the "Verification matrix" section. Every FR and every AS has at least one TR row, and each row states the observable result, side effects included. Cover the specified negative, boundary, authorization, failure and recovery behavior, not only the success path.
- Name the interface where the promise is made (a request, a form, a CLI call, a screen). Leave the concrete test selector to the plan; the spec stays free of technology.
- Mark each success criterion as a release gate or a post-launch measurement. Do not invent results for a measurement that has not happened.
- Leave the "Completion gate" section as written. It is binary.

### Project baseline

- When a hook before this command handed over a block that starts with `**Implements**:`, write that block directly below the `**Input**` line, unchanged.

{CORE_TEMPLATE}
