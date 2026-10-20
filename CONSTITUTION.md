# speckit-pro Constitution

## Inherited spirit

Specifications lead implementation: code serves specifications. The specification is the
shared language for intent, precise enough to build from, researched in context and refined
continuously. Feedback from implementation flows back into the specification.

speckit-pro carries this principle to the whole product: every feature specification serves
the product. Project memory records what the product is, how it is built and why decisions
were made. Product context precedes specification; architecture context precedes planning.
Conflicts go to the user, whose answers are retained. Finished features write lessons
automatically; contradictions become open questions without changing approved intent.

## Five promises

1. **Project memory with one home per fact.** `constitution.md` holds working rules,
   `product.md` the what, `architecture.md` the how and `decisions.md` the why.
2. **Consulted at the right moment.** Consult product before specify and architecture before
   plan. Put conflicts to the user and keep their answers.
3. **Automatic write-back preserves approved intent.** When converge reports `converged`
   and `Completion: DONE` is set, write-back applies new rows and merges that extend
   existing rows without changing their meaning, without asking the user. A row that
   contradicts an existing approved row is not applied: it becomes a new `Q-NNN` open
   question in `product.md`, citing both rows and the source feature. Every written
   row is tagged with its source feature. Only an approved `amend` changes meaning
   on purpose; code never silently redefines intent.
4. **Familiar Spec Kit, inherited, never forked.** Add through supported extension and preset
   surfaces, using wrap and append. Inherit new upstream releases and delete additions that
   upstream now supplies. Never copy or edit upstream files.
5. **DONE means the records hold together.** A small deterministic check rejects completion
   unsupported by the feature's own records. Analyze, converge and the user judge meaning.

## Working law

**Process weight follows change size.** Features take the full path. Small changes and bug
fixes take a light path. Keep only the process that helps preserve intent and useful memory.

## Spirit test

Before accepting a change, ask:

- Does it help remember or respect what the product is, how it is built, or why?
- Does the user remain the approver of meaning?
- Does it fit an extension or preset on upstream without copying upstream?
- Is a script trying to judge meaning? Move that judgment into a command or to the user.
- Does it depend on execution machinery or how tasks are carried out? Keep that outside this product.

## Non-goals

- A fork of Spec Kit, or a prepared copy of its commands and templates.
- A verification or attestation system: local records do not certify their own truth.
- An executor: speckit-pro neither schedules nor runs task execution.
- A judge of meaning in scripts: scripts check structure, citations and completion records.

## Delivery standards for speckit-pro itself

- Work on a branch per change; keep changes reviewable and never edit the main branch directly.
- Tests are the delivery gate. Run `python3 -m unittest discover -s tests` and the repository
  guard before delivery. Tests use no network or model calls.
- Use semantic versions for the extension and preset, and record releases in `CHANGELOG.md`.
- Keep scripts in `extension/scripts` and `preset` within 300 nonblank, noncomment lines
  combined. Prefer Python 3.11+ and its standard library.
- Install through the user's Spec Kit CLI using supported extension and preset commands.
- Commits in this repository name the user as the sole author and carry no AI attribution.
