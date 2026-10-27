# Changelog

## Unreleased

- The closing `Verification and convergence` phase only runs and records the Quality gates.
  Its "run converge" and "DONE check" tasks are gone: implement already runs converge after
  the tasks, so a task worker was running a second, cheaper review that appended and ticked
  tasks itself. A task that writes a failing test saves that run to its own log file, so
  test-first evidence survives parallel tasks.
- `tasks` never marks `[P]` on a task that depends on another task of its phase (such as
  an implementation that waits for its failing test), restoring upstream's "no
  dependencies on incomplete tasks" rule that the wrap had dropped. Each phase must end
  with every Quality gate passing, and a folder a gate needs must receive a file. `analyze`
  reports both.
- `install.sh` turns a folder that is not yet a Git repository into one, through the
  upstream Git extension's `initialize_repo.py` (repository plus first commit), so feature
  branches work from the first command. Existing repositories are left alone.
- `install.sh --agents claude` makes `.claude/skills` one folder link to
  `../.agents/skills` instead of one link per skill, so every agent shares one
  skills folder. Earlier per-skill links are replaced; other skills stop the
  installer with instructions.
- Documentation: add a command reference describing when to use each command,
  what it asks, writes and never does, and which commands run as hooks.

## 4.0.1 — 2026-10-20

- Documentation: drop the scripts line budget from the design note.

## 4.0.0 — 2026-10-20

- Build on Spec Kit 1.2.2 through extension hooks, command wraps and template appends.
- Share standard Agent Skills in `.agents/skills/` with optional relative Claude Code
  links; use Spec Kit's integration commands to select one managed integration.
- Add product Spirit, capability Serves citations, retained rejected options,
  Focus verdicts and 14 Delivery standards areas.
- Consult memory before specification and planning; approve intentional meaning
  changes through amend and recover observed behavior separately from intent.
- Keep full and light paths, stable IDs, test-first implementation, concrete
  Quality gates and append-only convergence remediation.
- Apply new and meaning-preserving lessons automatically after DONE; record
  contradictions as open questions and block sensitive memory before commit.
- Commit completed code, verification and memory together; ask before delivery.
- Configure upstream Git defaults, branch type/ticket naming and Conventional Commits.
- Keep structural memory and DONE checks read-only, using Python's standard library.
- Verify shared skills, Claude links and upstream composition with the installation
  check; document onboarding, overrides and check limitations in the README.
