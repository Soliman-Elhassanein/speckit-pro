# Adoption prompt

Paste the block below into a coding agent opened in the root folder of the target project. It works for an empty folder, a folder that holds only notes, and a project that already uses Spec Kit.

Nothing needs filling in. If this standard's folder moves, update the path that appears three times in the block.

```text
Set up Spec Kit in this project if it is missing, then adopt my Spec Kit standard.

The standard lives outside this repo at:
  /media/Data/Work/None College/Coding/speckit/
    speckit-universal-profile.md   (core, always applies)
    modules/                       (optional modules; section 12 of the core
                                    says when each one applies)
    preset/                        (my rules for the converge command)

Do these in order.

1. Look first. Inspect the folder: Git state, existing Spec Kit files
   (.specify/), agent folders, constitution, specs, code, and any notes or
   requirement documents. Change nothing yet.

2. Version control. If this is not a Git repository, run `git init`, add a
   sensible .gitignore, and commit what is already here as the first commit.
   If it is one, leave existing uncommitted work alone and keep it out of your
   commits. Git stays local; never push.

3. Spec Kit.
   - If .specify/ already exists, keep the integration and the command folder
     the project already uses. Do not install, add, or switch an integration.
   - If it does not exist, initialize with skills in .agents/skills:
       specify init --here --force --integration codex --integration-options="--skills" --script sh --ignore-agent-tools
     Confirm the only new top-level entries are .agents and .specify. Commit.
   The Spec Kit commands are the files in that folder. To run one, read its
   file and follow it. Never create a .claude directory, or any agent directory
   the project does not already use.

4. Copy the core profile into the repo, byte for byte:
   - if commands live in .agents/skills: to .agents/skills/speckit-standard.md
   - otherwise: to docs/speckit-universal-profile.md
   Read the copy completely.

5. Decide which optional modules apply, using section 12 of the standard and
   what you found in step 1. Copy only the applicable ones, byte for byte, to
   docs/modules/, and read them. Record every module in the adoption report as
   applicable, naming the sections that apply, or as N/A with a concrete
   reason. If the architecture or platform is not chosen yet, mark the modules
   that depend on it N/A for now and say when to re-evaluate them.
   Links in the copied files that point to files you did not copy will not
   resolve; note that in the report instead of fixing it.

6. Add my converge rules to the converge command the project uses:
   - generic integration with a custom folder, such as .agent/commands:
       sh "/media/Data/Work/None College/Coding/speckit/preset/apply-converge.sh" <path to the installed converge command>
   - any built-in integration, such as .agents/skills:
       specify preset add --dev "/media/Data/Work/None College/Coding/speckit/preset"
   Confirm the converge command now contains the heading
   "Universal profile rules".

7. Read the project's own material: vision, requirement, design, and research
   documents, and any existing specs. Where documents conflict, record the
   conflict instead of choosing silently.

8. Before writing or amending the constitution, ask me about each open product
   decision that would change a constitutional principle, such as where data
   lives, who the users are, or which platforms are targets. Ask one question
   at a time, each with your recommendation. Record other open decisions as
   open.

9. Constitution. If none exists, create it by following the constitution
   command. If one exists, amend it in place as section 3 of the standard
   describes. Build the project's principles from its own material and from
   section 3.

10. Follow the adoption transaction in section 2 of the standard: synchronize
    the templates in .specify/templates and every installed command. In each
    command file, add one short section that tells the reader to read the
    repo's copy of the standard before acting and names the sections that
    govern that command. Point to the standard; do not copy its rule text.
    Keep each file's frontmatter and existing steps intact.

11. Existing features. If the project already has specs, preserve their IDs,
    checked tasks, decisions, and evidence. Repair only what adoption needs,
    such as missing AS and TR identifiers and the verification matrix, as
    section 1.2 of the standard describes. Do not regenerate them.

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
accurately; they are NOT RUN if you ran none. Then list the agent command
folder recursively and show me the output, and name the command I should run
next.
```
