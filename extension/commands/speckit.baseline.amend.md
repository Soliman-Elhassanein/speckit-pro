---
description: "Approve project-memory amendments row by row from proposals, files or a feature folder"
---

# Amend project memory

Consider `$ARGUMENTS`. This is the only command that changes project meaning.
Converge also writes non-conflicting lessons automatically after DONE; only amend
may intentionally change approved meaning. The checker remains read-only.

Memory has one home per fact beside `.specify/memory/constitution.md`:
`product.md` holds Spirit (purpose, users, PR promises, non-goals), capabilities and
open questions; `architecture.md` holds stack, parts, design constraints, interfaces
and Delivery standards; `decisions.md` holds choices, reasons and rejected options.
The constitution holds how-we-work rules. Blocking Delivery rows alone hold delivery
non-negotiables. Feature detail stays in the feature folder.

Memory is committed and often public. Never write absolute or home paths, usernames,
hostnames, IP addresses, internal URLs, emails, ports of private services, credentials,
tokens, keys or secrets, or any value copied from `.env` / config files. Describe
things generically (`the config file`, `the database host`); repo-relative paths are fine.
Apply this to source tags, evidence and questions too. Run the blocking privacy check
before saving any memory for commit; rewrite a hit generically or drop the row.

1. Read constitution and the three memory files, including rejected options. For first
   creation, use `.specify/extensions/baseline/templates/` as proposals, removing
   placeholder rows before saving. Keep all 14 Delivery areas; unresolved areas stay
   undecided. Never silently promote observed behavior into approved intent.
2. Accept proposals from the current conversation, a file (any report), or a feature
   folder. Treat every input as a proposal, even when it says a decision was made.
   A decision-record file has one decision and this shape, with all sections present
   even when empty:

   ```markdown
   # Decision: <short title>
   Date: YYYY-MM-DD
   Question: <question to resolve>

   ## Decision
   <choice and reason>

   ## Rejected options
   | Option | Why not |
   |---|---|

   ## Open questions
   | Question | Blocks |
   |---|---|

   ## Sources
   - <file:line, URL or document; marked verified or unverified>
   ```

   Preserve alternatives and their reasons, unresolved questions and source confidence;
   do not invent missing rationale. Any report can supply the same facts in prose.
3. For a feature folder, read spec (including Focus), plan, research, tasks and
   verification. Extract write-back proposals: capabilities, project-wide decisions
   from research's Decision / Rationale / Alternatives, architecture parts/rules,
   Delivery changes and answered open questions. Tag each with its source feature
   and classify **new**, **merges with** or **contradicts** an existing row. Deduplicate
   proposals; merge into the fact's existing home. Completion is not approval.
4. Show exact proposed rows/cells grouped by file, with old/new values and evidence
   paths. Include Spirit edits explicitly, a capability's Serves PR and dependencies,
   and a decision recording each choice. IDs CAP-, PR-, AR-, D-, Q- use at least three
   digits, allocating the next unused number without renumbering existing entries.
   Put conflicting sources to the user; ask only blocking questions and park others
   under Open questions. **Wait for the user's approval of each row before writing.**
5. Apply only approved changes. Record conflict answers and “do it anyway” overrides
   in decisions.md, including the reason and scope. A Spirit change must explicitly
   amend Spirit after approval; an override does not silently redefine it. Never
   justify code by rewriting intent without that choice being approved.
   Retain retired/superseded capabilities and answered questions (`answered by D-NNN`).
   Decisions retain their question, choice, rationale and rejected options; a changed
   decision gets a new row and the predecessor becomes `superseded by D-NNN`.
6. Bump each changed file's semantic version, including decisions.md: MAJOR for changed
   existing behavior/boundaries, MINOR for additions, PATCH for wording. Set Last amended.
7. Run `python3 .specify/extensions/baseline/scripts/baseline_check.py`. Fix structural
   errors caused by these edits without inventing approval. Report changed files,
   versions, rows, decisions, open questions and check results. Review affected specs
   and plans; commit under the project's delivery rules when requested.
