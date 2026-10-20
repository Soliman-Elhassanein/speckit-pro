---
description: "Apply approved branch type and ticket naming after upstream branch creation"
---

# Branch naming

This after_specify hook uses the branch already created by the `speckit-git-feature` command.
Never create another branch or edit upstream files. Consider the original request
and context's chosen full/light path. Also apply this command explicitly for light
changes on an existing numbered branch; if no branch id is available, ask for it
rather than inventing a spec or ticket.

1. Read the current branch with `git branch --show-current` and the current feature
   folder from upstream's feature state. Skip renaming when Git is unavailable; still run step 5. Never rename
   main, master, a detached HEAD or a branch unrelated to this request.
2. Default type is feature for the full path; choose fix for a bug, hotfix only for
   an explicitly urgent production repair, or refactor, docs, chore from the request.
   An explicit user type wins. Use only feature, fix, hotfix, refactor, docs, chore.
3. Use the ticket id exactly when supplied (for example APP-142); otherwise retain
   upstream's spec number (007). Keep the upstream short slug. Desired name:
   `<type>/<id>-<short-name>`. Do not change the feature folder, number, feature.json
   or SPECIFY_FEATURE: upstream feature discovery is independent of branch naming.
4. If a rename is needed, validate the desired name with `git check-ref-format
   --branch <desired name>` then use `git branch -m <desired name>`. Quote the name
   as a single argument; never use force or overwrite an existing branch. Report
   errors and stop for resolution. Report the resulting name and id for Refs footers.

5. Run `python3 .specify/extensions/baseline/scripts/baseline_check.py` with
   `--feature <feature folder>` when known, including when the branch was unchanged.
