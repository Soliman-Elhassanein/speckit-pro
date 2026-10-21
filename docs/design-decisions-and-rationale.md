# Design note

speckit-pro extends Spec Kit's specification-first principle to product-wide intent.
Product memory precedes specification; architecture memory precedes planning.
Only the user-approved amend command changes approved meaning. Finished features
write new and meaning-preserving lessons automatically after DONE; contradictions
become open questions. Privacy checks block sensitive memory before commit. One fact has one home, and rejected choices retain reasons.

The extension owns memory commands, hooks, templates and the read-only checker.
The preset adds feature rules through wrap and append. The installer delegates
installation and lifecycle to the user's CLI. The Git extension owns branch
creation and conventional type generation; configuration supplies defaults, and a
small after_specify hook applies type/ticket overrides by renaming the current
branch. This avoids depending on unverified extension-command wrapping support.

The DONE check shares the memory check's entry point. It validates recorded structure, never truth or meaning. Analyze
and converge judge scope, coverage and architecture. A single verification.md holds
gates, exit codes, log paths, gaps and convergence; no second completion record.

AS/TR IDs, the verification matrix,
optional domain guidance and derived views stay deferred until real use shows a
need. Real CLI composition needs the install/upgrade check and a first feature run;
offline tests cannot establish it.

One shared `.agents/skills/` folder avoids diverging copies when Spec Kit applies
presets and extensions only to its default integration. The installer uses the
Codex integration to render standard skills and Spec Kit's lifecycle commands to
remove other managed integrations. Claude Code receives one relative folder link;
this follows the single-copy design of `npx skills`.

Design inspirations: Archive, Spec Roadmap's debrief, Canon, ProductShape and
OpenSpec informed feature-to-memory write-back; adrkit informed retaining rejected
options in context; Spec Roadmap's outcomes informed capability-to-promise links.
These are design credits; no implementation from those projects is shipped.
