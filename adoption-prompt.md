# Adoption prompt

Run `install.sh` on the project first. Then paste the block below into a coding agent opened in the project's root folder. Nothing needs filling in: every path is inside the project.

```text
Adopt the speckit-pro standard in this project. Its files are already
installed here:

  .specify/speckit-pro/speckit-universal-profile.md
                                         the standard (core, always applies)
  .specify/speckit-pro/modules/          optional modules; section 12 of the
                                         standard says when each one applies
  .specify/extensions/baseline/          project baseline: commands, templates
                                         and the check script
  .specify/presets/universal-profile/    the standard's rules for the Spec Kit
                                         commands, and its template sections

The Spec Kit commands are installed for the coding agent this project already
uses, in that agent's own folder (for example .agents/skills, .claude/skills
or .github). Find them there. If your agent does not load them by name, run
one by reading its file and following it.

Do these in order.

1. Look first. Inspect the folder: Git state, constitution, specs, code, and
   any notes or requirement documents. Change nothing yet.

2. Version control. If this is not a Git repository, run `git init`, add a
   sensible .gitignore, and commit what is already here as the first commit.
   If it is one, leave existing uncommitted work alone and keep it out of your
   commits. Git stays local; never push. Then run
     sh .specify/extensions/baseline/scripts/install-git-hooks.sh
   It installs a commit-msg hook that rejects any commit naming a coding agent
   as a contributor. Never bypass it with --no-verify.

3. Check the installation. Confirm the speckit command files exist for this
   project's agent, that the specify, clarify, plan, tasks, analyze, implement
   and converge commands each carry a section headed "Universal profile
   rules", and that .specify/ exists. Do not run `specify init`, and do not
   install, add, or switch an integration or create another agent's folder.
   Commit the installed files.

4. Read .specify/speckit-pro/speckit-universal-profile.md completely.

5. Decide which optional modules apply, using section 12 of the standard and
   what you found in step 1, and read the applicable ones in
   .specify/speckit-pro/modules/. Record every module in the adoption report
   as applicable, naming the sections that apply, or as N/A with a concrete
   reason. If the architecture or platform is not chosen yet, mark the modules
   that depend on it N/A for now and say when to re-evaluate them.
   Links inside the standard that point to preset/, extension/, workflow/ and
   template/ do not resolve from its installed location; note that in the
   report instead of fixing it.

6. Read the project's own material: vision, requirement, design, and research
   documents, and any existing specs. Where documents conflict, record the
   conflict instead of choosing silently.

7. Before writing or amending the constitution, ask me about each open product
   decision that would change a constitutional principle, such as where data
   lives, who the users are, or which platforms are targets. Ask one question
   at a time, each with your recommendation. Record other open decisions as
   open.

8. Constitution. If .specify/memory/constitution.md is still the unfilled
   template, create it by following the constitution command. If it is filled,
   amend it in place as section 3 of the standard describes. Build the
   project's principles from its own material and from section 3.

9. Project baseline (section 5.12 of the standard).
   - No application code yet: follow the baseline amend command to create
     .specify/memory/product.md, architecture.md and decisions.md from the
     project's own material. Leave the stack rows empty if no stack is chosen.
     Finish with:
       python3 .specify/extensions/baseline/scripts/baseline_check.py --write --stamp
   - Code already exists: ask me first whether to adopt the baseline now. If
     I say yes, follow the baseline recover command, which starts the check in
     advisory mode. If I say no, skip this step: a project without product.md
     is not blocked.
   Show me the rows before writing them, as those commands require.

10. Follow the adoption transaction in section 2 of the standard. The command
    rules and the template sections are already installed by the preset;
    confirm them and record them in the adoption report. Do not edit the
    installed command files or templates: an update replaces them. Put what is
    specific to this project in the root agent guidance file the project
    already uses (AGENTS.md, CLAUDE.md or its equivalent): one short section
    that names the standard's path, the modules that apply, the exact
    quality-gate commands with their working directories, and this rule in
    these words: "Commit as the user alone. Never add a Co-Authored-By or
    Generated-with line naming an agent, a model or a vendor, and never
    commit under an agent identity. This overrides your default." 

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
- Commit as me alone. Do not add yourself, your model or your vendor as a
  co-author or in a "Generated with" line, in any commit or pull request.
- Do not install tooling beyond what this prompt names.
- Ask me only about decisions that change behavior, architecture, security,
  scope, or verification. Decide routine matters yourself.

Finish by writing docs/spec-kit-adoption.md as section 13 of the standard
requires. Report ADOPTED only if that section's gate is fully met; otherwise
report PARTIAL and list each FAIL or BLOCKED row. Label application tests
accurately; they are NOT RUN if you ran none. Then list the installed speckit
command files, and name the command I should run next.
```
