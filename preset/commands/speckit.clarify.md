---
description: "Resolve every material ambiguity in the spec, in rounds, and record each answer and each deferred point."
strategy: wrap
---

## Universal profile rules

These rules come from the Spec Kit Universal Adoption and Execution Profile (section 5.4). Where a stock step below says something different, these rules win.

- **There is no cap on the number of questions.** Ignore the stock limit of five. Ask in rounds of up to five questions, one question at a time, each with your recommendation taken from the repository. After a round, re-scan the spec and start another round while a material point is still open.
- Stop when every material point is resolved or the user defers what is left. A point is material when its answer changes behavior, acceptance, security, scope or verification. Do not ask about minor implementation preferences.
- Ask one question per root cause. Do not ask again what the spec, the constitution or the project baseline already settles.
- Write each accepted answer into the spec at once, remove what it contradicts, and update the affected AS and TR rows and the verification matrix.
- Record each deferred point in the spec as an open point, with what it blocks. When `.specify/memory/product.md` exists, recommend parking it as an open question through the baseline amend command, so that it is not lost and blocks the capability it concerns.

{CORE_TEMPLATE}
