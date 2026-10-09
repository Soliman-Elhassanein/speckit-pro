---
description: "Build the first baseline for a project that already has code, from evidence, for the user to approve"
---

# Recover a Baseline from Existing Code

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Use this once, in a project that has code but no baseline, or to map folders the check reports as unmapped. Existing code is evidence of what was built. It is not proof of what the product should do: nothing here becomes approved until the user says so. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`.

## Start in advisory mode

A project that already has code will not pass the check on its first day. Before anything else:

```sh
CHECK --mode advisory
```

The check then reports without stopping work. When it runs clean, tell the user and offer `CHECK --mode blocking`.

## Rule: no evidence, no claim

Every row you propose names the file or folder that shows it. If you cannot point to evidence, do not write the row; ask the user or park it as an open question.

## Steps

### 1. Partition

```sh
CHECK --scan
```

The script lists every top-level folder of tracked code and the files at the repository root, with file counts, build manifests and file types, and names the hidden folders. It reads names only. Use this list as the complete set to account for: every folder ends up mapped to a part, or the user confirms it is not product code.

### 2. Draft the architecture

For each folder, read enough of it to say what it is. Draft:

- **Stack**: one row per choice the manifests and lockfiles show.
- **Parts and boundaries**: one row per part, with its Paths from the scan, what it owns, and what it imports from. Root files and hidden folders that are product code, such as an entry point or deployment workflows, belong to a part too. List what is not product code on the `**Not code**:` line.
- **Architecture rules**: only rules the code visibly and consistently follows, each marked not blocking until the user says otherwise.

### 3. Draft the product

From the entry points, screens, routes, commands and tests, draft one capability row per promise the code keeps. Give every one the decision `proposed`. Where existing specs describe the behavior, name the owning spec; otherwise leave `-`.

### 4. Draft the decisions

Record only decisions the repository itself explains: a design note, a commit message, a comment that says why. Do not invent reasons. A choice with no recorded reason becomes an open question for the user: "Was X chosen on purpose?"

### 5. Review with the user

Show the drafts grouped by file, each row with its evidence path. Ask the user to confirm, correct or drop rows; for capabilities, ask which ones to mark `approved`. Take the corrections in batches of related rows, not one question per row.

### 6. Write and stamp

Run the baseline amend command with the confirmed rows. Then record the starting point:

```sh
CHECK --write --stamp
```

Report: folders mapped, folders left out and why, rows approved, rows still `proposed`, and open questions.
