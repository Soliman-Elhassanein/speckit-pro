---
name: speckit-baseline-review
description: 'Before converge: review the finished code against the architecture rules and boundaries, and turn violations into tasks'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Soliman-Elhassanein
  source: baseline:commands/speckit.baseline.review.md
---

# Review Code Against the Architecture

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

This command runs as a hook before converge, so its findings are open tasks when convergence is judged and the feature cannot be marked done over them. It reads code and the baseline. Its only file write is appending tasks to the current feature's `tasks.md`. It never edits code, the spec, the plan or the baseline. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`.

## Steps

### 1. Get the scope from the script

```sh
CHECK --touched <current spec folder>
CHECK --run-rule-checks
```

The first command lists every file changed since the spec's baseline commit, the part that owns each one, every architecture rule, and the decisions that govern those paths. The second runs the rules that have an executable check. Review that scope; do not widen it.

### 2. Review

For the changed files, check each of these and record a finding only where the code shows the problem:

- **Rules**: each architecture rule, one by one, against the changed code.
- **Boundaries**: a part importing from, or reaching into, a part its "May depend on" cell does not allow.
- **Ownership**: a second copy of data, a rule or a check that another part owns.
- **Decisions**: code that does what an accepted decision ruled out, or what a rejected option described.
- **Unmapped**: a changed file that no part owns.
- **Plan**: an impact beyond what `plan.md` declared under "Architecture impact".

Every finding names the rule, part or decision ID, and the file and line that show it.

### 3. Act on findings

| Finding | Action |
|---------|--------|
| Breaks a rule marked Blocking, or a failed blocking check | Report it first. The feature is NOT DONE until it is fixed. Append the fix as a task. |
| Breaks any other rule, boundary or decision | Append a refactor task. Work may continue. |
| The code is right and the baseline is behind | Do not edit the baseline. Append a task: "decide: amend <ID> or change the code", for the user. |
| Unmapped file | Append a task to map it through the baseline amend command. |

Append tasks at the end of `tasks.md` under a heading `## Architecture review`, continuing the task numbering, one line each:

```markdown
- [ ] T0NN <imperative fix> per <AR-NNN | part name | D-NNN> (<file>:<line>)
```

Do not duplicate an open task that already covers the finding; cite it. With no findings, leave `tasks.md` unchanged.

### 4. Report

State the files reviewed, the rules checked, each finding with its ID and location, the tasks appended, and whether anything blocking remains.