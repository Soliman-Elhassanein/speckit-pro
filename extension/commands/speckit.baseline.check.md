---
description: "Run the deterministic baseline check and recalculate delivery status"
---

# Baseline Check

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

This command runs a script. The script decides; do not replace its result with your own judgment.

## Run

From the repository root:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py          # check only
python3 .specify/extensions/baseline/scripts/baseline_check.py --write  # also recalculate Delivery
```

- **Before implement**: run the check-only form.
- **After converge, or on request**: run with `--write`.

## What it checks

- IDs are unique, and every ID cited in a spec or plan exists.
- Every spec names the capabilities it implements, and each one is `approved`.
- Each capability's owning spec exists and names that capability.
- No spec or plan cites a decision that is `rejected` or superseded.
- Links inside the three baseline files resolve.
- The Delivery column matches the owning spec's `verification.md`: `verified` only when it says `Completion: DONE`.

## Act on the result

- **Exit 0**: report "baseline check passed" and continue.
- **Exit 1**: show the errors exactly as printed. Before implement, stop: implementation does not start until they are fixed. A missing or wrong line in a spec or plan is fixed in that file. Anything that needs a change to `product.md`, `architecture.md` or `decisions.md` goes to the user through the baseline amend command; do not edit those files here.

With `--write`, the script changes only the Delivery cells of `product.md`. Commit that change with the work that caused it.
