---
description: "Choose full or light path, load memory, resolve focus and delivery conflicts before specify and plan"
---

# Project context

Consider `$ARGUMENTS`. This hook runs before specify and plan. It reads memory;
only the `speckit-baseline-amend` command changes its meaning after row-by-row user approval.

Memory is committed and often public. Never write absolute or home paths, usernames,
hostnames, IP addresses, internal URLs, emails, ports of private services, credentials,
tokens, keys or secrets, or any value copied from `.env` / config files. Describe
things generically (`the config file`, `the database host`); repo-relative paths are fine.
Apply this to source tags, evidence and questions too. Run the blocking privacy check
before saving any memory for commit; rewrite a hit generically or drop the row.

1. Run `python3 .specify/extensions/baseline/scripts/baseline_check.py`, using
   `--feature <feature folder>` when known. Report missing files, duplicate IDs and
   invalid references explicitly; incomplete context is not authoritative. If memory
   or Spirit is missing, propose amend (recover for existing code) before specification.
2. Choose exactly two paths: **full** for features (specify → clarify → plan → tasks →
   analyze → implement → converge), or **light** for small changes and bug fixes.
   Light: name the approved behavior and what must stay unchanged, reproduce a bug
   with a failing test where applicable, make the change and run applicable gates.
   Stop the calling specify/plan flow for light changes; do not create a feature spec
   just for process. For light changes, invoke baseline.branch on the existing
   numbered branch to apply the request's type and ticket id. Both paths consult memory and require approval of meaning changes.
3. Load product Spirit (purpose, named users, all PR promises and non-goals), capability
   index, affected capabilities/dependencies and open questions, plus constitution.
   Load product decisions and scoped architecture decisions, **including rejected
   options and why**. Ordinary rejected prose is context, not a governing citation.
   Do not silently revive rejected options. Follow applicable local contract links;
   missing linked material must be reported.
4. Give **one focus verdict per request**, including light changes:

   | Verdict | Action |
   |---------|--------|
   | fits | Name the user and the PR promise it serves. |
   | stretch | Propose the smallest version serving a promise, or defer. Resolve scope with the user before proceeding. |
   | distraction | Stop, explain the non-goal or missing promise, and say where the request belongs. |
   | spirit change | Stop for approved amend of the Spirit section, recorded in decisions.md, before proceeding. |

   Put conflicts, duplicates, unavailable dependencies, blocking questions and requests
   to reopen rejected options to the user with a recommendation. Retain answers through
   amend; a “do it anyway” requires an accepted decision explicitly recording the
   override and its reason. Do not treat this as implicit permission to rewrite Spirit.
5. For the full path hand the resolved verdict to specify, which must write:

   ```markdown
   ## Focus

   Verdict: fits | stretch | distraction | spirit change
   User: <named user>
   Reason: <resolved scope and why it serves the product>
   **Promises**: PR-NNN
   **Override**: none
   ```

   Use real PR IDs; when proceeding under an approved override, use
   `**Override**: D-NNN` citing the accepted override decision. Either a promise or
   an override is required. Do not repeat the gate as a second verdict before plan;
   load the existing Focus and revisit it only if the request changes.
   Hand over `**Implements**: CAP-NNN` and `**Product rules**: PR-NNN` as dedicated
   citation lines; capabilities must be approved. A missing capability requires amend.
6. Before plan, inventory the files the design touches. Load stack, affected parts and
   boundaries, all architecture rules, Delivery standards, scoped decisions with
   rejected options and reasons, and applicable interfaces/contracts. Planned part
   paths are information only; no code needs to exist yet. Before specify, also load
   any of these needed to resolve the request's conflicts or delivery impact, keeping
   implementation choices out of the product spec.
7. Ask about an **undecided** Delivery area when the feature first touches it. Propose
   a rule, Check and Blocking value (or n/a with reason); use amend to keep the answer.
   Blocking rows are the non-negotiables and have no second home. Add each applicable
   decided Check command to plan's Quality gates table; do not execute it here.
8. Before plan, label architecture impact `none`, `extends` or `changes`. For extends
   or changes, resolve with the user: fit the plan to approved architecture or approve
   an amendment first. Hand over `**Architecture impact**`, `**Architecture rules**`,
   `**Decisions**` and `**Parts**` lines. Cite governing AR and accepted D IDs or `none`,
   and name every affected part. Retain the Focus section as the scope boundary.
