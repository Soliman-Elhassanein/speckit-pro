---
description: "Assess intent, architecture and gates; append remediation, write back after DONE and ask before delivery."
strategy: wrap
---

## speckit-pro rules

- Assess current code, tests and verification.md against spec, plan and tasks.
  Inspect assertions at the interface where behavior is promised; names and checked
  boxes alone are not coverage. Missing, stale, failed or blocked results are gaps.
- Check architecture rules, ownership, allowed dependencies and part boundaries,
  accepted decisions and blocking Delivery standards. Never rewrite approved intent
  to match code; contradictions require the user's choice through amend or repair.
- Only append deduplicated remediation to tasks.md: cite existing open tasks instead
  of duplicating them; leave old task text and checkboxes intact. Each new task has
  a new ID, affected paths, requirement references, dependencies and validation.
  During assessment do not edit code, spec, plan or memory. Record the outcome
  in verification.md; safe relevant tests may be run.
- Report exactly one outcome:
  - `tasks_appended`: new uncovered remediation appended; return to implement.
  - `gaps_remaining`: no new tasks, but open work, decisions or verification gaps
    remain; cite them and report NOT DONE.
  - `converged`: no gaps, all required current gates pass and every task is checked.
    No new tasks alone does not imply convergence.
- Only after `converged`, set `Completion: DONE` in verification.md and run
  `python3 .specify/extensions/baseline/scripts/baseline_check.py --done --feature <feature-folder>`.
  On failure report NOT DONE and return to remediation. Never write back or deliver
  for any other outcome or before DONE.
- Write-back is automatic after that check passes; do not ask for approval. Read
  existing memory and the feature's spec, plan, upstream research.md and verification.
  Include capabilities with `Serves` PR citations, project-wide decisions with
  Decision / Rationale / Alternatives, new architecture rules or parts, and answered
  open questions. Classify each candidate against approved memory:
  - `new`: write directly into the fact's home.
  - `merges with <row>`: extend that row only when its meaning stays unchanged.
  - `contradicts <row>`: leave the approved row intact; instead write a new Q-NNN
    open question in product.md citing both the approved row and the conflicting
    feature row (repo-relative file and heading if it has no ID), and the feature.
    Nothing waits for the user; only amend can intentionally change meaning.
  Deduplicate against existing rows/questions so reruns do not repeat write-back.
  Allocate next unused IDs without renumbering; tag every written or extended row
  with `Source feature: <repo-relative feature-folder>` in its descriptive cell.
  Retain rationale and alternatives, mark completed capabilities approved, and use
  `answered by D-NNN` only with a supported accepted decision. Keep unanswered
  questions open. Follow amend's version and Last amended rules. If nothing applies,
  say so. Never infer a new Spirit or Delivery rule from implementation.

Memory is committed and often public. Never write absolute or home paths, usernames,
hostnames, IP addresses, internal URLs, emails, ports of private services, credentials,
tokens, keys or secrets, or any value copied from `.env` / config files. Describe
things generically (`the config file`, `the database host`); repo-relative paths are fine.
Apply this to source tags, evidence and questions too. Run the blocking privacy check
before saving any memory for commit; rewrite a hit generically or drop the row.

- Run the blocking memory and DONE check again on the written changes before committing.
  A privacy hit means rewrite the row generically or drop it, including any source
  quotation in a conflict question; never commit a hit. Fix structural errors and
  rerun. If checks cannot pass, stop without committing or delivering.
- After write-back and successful checks, commit the feature's code, verification.md
  and memory changes together on the feature branch as one Conventional Commit under
  the project's Git & branching rule. Inspect the diff; exclude unrelated changes.
  Never commit on the target branch. Use the spec for the subject and a
  `Refs: <ticket or spec>` footer. If a commit fails, stop before delivery.
- Then read the Git & branching Delivery row and **ask the user before delivery**:
  - pull requests: ask to push the feature branch and open a PR into the target.
    After approval, push and use `gh pr create` for a GitHub remote (otherwise the
    project's configured PR tool). Use a Conventional Commit title from the spec;
    body from verification.md with gates and exit codes, and a
    `Refs: <ticket or spec>` footer.
  - merge locally: ask to merge into the target branch and delete the feature branch;
    only after approval perform the merge and delete after a successful merge.
  - undecided: ask which method and target, record the answer once in that Delivery
    row as the user's explicit choice; run the memory check and include it in the
    feature commit (amend that commit if already created). Ask for delivery approval
    if the answer only selected a method rather than authorizing delivery.
  Never infer a target if it is unknown. If the user declines, stop and give the
  exact commands to deliver later using the known branch and target. Never change
  branch protection, CI or deployment. Delivery is the final step, only after DONE.

{CORE_TEMPLATE}
