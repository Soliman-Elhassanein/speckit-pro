# Adoption prompt

Run `install.sh` on the project first. Then paste the block below into a coding agent opened in the project's root folder. Nothing needs filling in: every path is inside the project.

```text
Adopt the speckit-pro standard in this project. Its files are already
installed here:

  .agents/skills/speckit-*/SKILL.md      the Spec Kit commands (run one by
                                         reading its file and following it)
  .agents/skills/speckit-standard.md     the standard (core, always applies)
  .specify/speckit-pro/modules/         optional modules; section 12 of the
                                         standard says when each one applies
  .specify/extensions/baseline/          project baseline: commands, templates
                                         and the check script

Do these in order.

1. Look first. Inspect the folder: Git state, constitution, specs, code, and
   any notes or requirement documents. Change nothing yet.

2. Version control. If this is not a Git repository, run `git init`, add a
   sensible .gitignore, and commit what is already here as the first commit.
   If it is one, leave existing uncommitted work alone and keep it out of your
   commits. Git stays local; never push.

3. Check the installation. Confirm .agents/skills holds the speckit skills and
   speckit-standard.md, and that .specify/ exists. Do not run `specify init`,
   and do not install, add, or switch an integration. Never create a .claude
   directory or any other agent directory. Commit the installed files.

4. Read .agents/skills/speckit-standard.md completely.

5. Decide which optional modules apply, using section 12 of the standard and
   what you found in step 1. Copy only the applicable ones, byte for byte,
   from .specify/speckit-pro/modules/ to docs/modules/, and read them. Record
   every module in the adoption report as applicable, naming the sections that
   apply, or as N/A with a concrete reason. If the architecture or platform is
   not chosen yet, mark the modules that depend on it N/A for now and say when
   to re-evaluate them.
   Links inside the standard that point to modules/, preset/ and extension/
   do not resolve from its installed location; note that in the report
   instead of fixing it.

6. Read the project's own material: vision, requirement, design, and research
   documents, and any existing specs. Where documents conflict, record the
   conflict instead of choosing silently.

7. Before writing or amending the constitution, ask me about each open product
   decision that would change a constitutional principle, such as where data
   lives, who the users are, or which platforms are targets. Ask one question
   at a time, each with your recommendation. Record other open decisions as
   open.

8. Constitution. If .specify/memory/constitution.md is still the unfilled
   template, create it by following the constitution skill. If it is filled,
   amend it in place as section 3 of the standard describes. Build the
   project's principles from its own material and from section 3.

9. Project baseline (section 5.12 of the standard).
   - No application code yet: follow the baseline amend skill to create
     .specify/memory/product.md, architecture.md and decisions.md from the
     project's own material. Leave the stack rows empty if no stack is chosen.
   - Code already exists: follow the baseline recover skill instead.
   Show me the rows before writing them, as those skills require. Finish with:
     python3 .specify/extensions/baseline/scripts/baseline_check.py --write --stamp

10. Follow the adoption transaction in section 2 of the standard. The
    specify, plan, tasks, analyze, implement and converge skills already carry
    the standard's rules under the heading "Universal profile rules", and the
    spec, plan and tasks templates already gain its sections from
    .specify/presets/universal-profile/templates/. Confirm both and record
    them in the adoption report. Do not edit those skills or templates. In
    each remaining stock SKILL.md (constitution, clarify, checklist,
    taskstoissues), add one short section that tells the reader to read
    .agents/skills/speckit-standard.md before acting and names the sections
    that govern that command. Point to the standard; do not copy its rule
    text. Keep each file's frontmatter and existing steps intact.

11. Existing features. If the project already has specs, preserve their IDs,
    checked tasks, decisions, and evidence. Repair only what adoption needs,
    such as missing AS and TR identifiers, the verification matrix, and the
    Implements line, as section 1.2 of the standard describes. Do not
    regenerate them.

Limits:
- Do not change product scope or settled decisions.
- Do not choose a technology stack, write application code, start planning, or
  create a new feature spec. I will start the next step myself.
- Do not move, rename, or edit my existing documents, except where step 11
  requires it.
- Commit coherent units with reviewed, explicit paths.
- Do not install tooling beyond what this prompt names.
- Ask me only about decisions that change behavior, architecture, security,
  scope, or verification. Decide routine matters yourself.

Finish by writing docs/spec-kit-adoption.md as section 13 of the standard
requires. Report ADOPTED only if that section's gate is fully met; otherwise
report PARTIAL and list each FAIL or BLOCKED row. Label application tests
accurately; they are NOT RUN if you ran none. Then run `ls -R .agents`, show
me the output, and name the skill I should run next.
```
