# Troubleshooting without weakening controls

| [Previous: dependency maintenance](3-maintain-dependencies.md) | [Next: annotated solutions](../solutions/README.md) |
|:---|---:|

## Why it matters

A workaround that removes the control also removes the evidence you came to collect. Preserve your work, diagnose the failure, and record incomplete outcomes honestly.

## Setup and accounts

| Symptom | Check and recovery |
|---|---|
| Cannot create public repo or change settings | Confirm the signed-in account, admin access, email verification, and employer/organization policy. Managed users cannot create public repositories. Use an eligible personal account only if permitted; otherwise arrange approved observation and mark individual work incomplete. |
| Git authentication fails | Confirm the learner origin and your existing credential helper or VS Code browser sign-in. Use the web route if local authentication is restricted. Never paste a PAT into code/URLs or change global work identity for this lab. |
| Author identity unknown or wrong commit email | Authentication does not set your commit author. Follow [Step 0's repository-local identity check](../0-setup.md#terminal-route), using the exact noreply address shown in your GitHub email settings. Do not change global corporate settings; the helper never changes identity. |
| Helper rejects origin | It accepts direct GitHub.com HTTPS/SSH learner URLs and rejects upstream, aliases, embedded credentials, multiple origins, or a different push destination. Inspect `git remote -v` yourself; do not share embedded credentials. Correct the clone intentionally, not by asking the helper to mutate remotes. |
| Wrong branch, detached HEAD, or Git operation in progress | Finish your work on its intended branch and resolve or deliberately abort the existing operation. Then use clean `main`. The helper does not reset, stash, or change your identity. |
| Unrelated files or conflicting workflows | Review and preserve them. Use a fresh original-template learner copy if appropriate, or manually reconcile the two workflows. Identical kit files are a no-op; differing files are never overwritten by the helper. |
| Baseline fingerprint mismatch | An original-template update or local application change needs review. Report the exact path, kit version, and source revision. The organizer must refresh and retest the companion; do not switch to an alternate application template or replace the app with old files. |
| Helper refuses after lesson 3 | Expected: the application fingerprint changed because you fixed it. Use the resume guide; the helper is for initial setup only. |
| Kit files appear as unrelated changes | Extract the fetched archive outside the learner clone. Move only that kit directory yourself after checking its contents; do not delete learner files. |
| Starter PR already exists | Resume it and inspect its current branch/checks. For a closed/merged PR, follow [Resume](0-resume.md). |

## Checks and findings

| Symptom | Check and recovery |
|---|---|
| No CI run | Confirm `.github/workflows/ci.yml` is committed on remote `main`, Actions is permitted, and the YAML matches the kit. Use **Run workflow > main**. Do not use a non-main manual run as baseline evidence. |
| API dependency resolution fails | Read the first pip conflict; check the reviewed constraints and direct requirements. Update the snapshot through a PR when appropriate; never install the lab fixture. |
| Client build fails with Node version error | This track uses Node 24. Astro 6 requires Node >=22.12; older Pets examples using Node 20 are not the supplied workflow. Preserve `package-lock.json` and use `npm ci`. |
| Required check is missing | Confirm the workflow exists on both PR/base branches, the PR targets `main`, and exact job names are `api-tests`, `client-build`, `dependency-review`. These starters have no path filters. Rerun a real PR event; don't mark a missing check successful. |
| CodeQL is pending or failed | Inspect the analysis run, languages, and default setup settings. Avoid installing advanced setup alongside default setup. Wait/retry the failed analysis; neither silence nor a failed scanner proves the finding is gone. |
| Expected debug finding absent | Confirm the pinned original source and Python analysis. The code might already be fixed or query behavior may have changed. Report drift; do not inject a new vulnerable endpoint. |
| Default-branch alert remains after PR fix | Check the PR's latest analysis first. The default-branch alert closes after safe merge and successful default-branch analysis, not just after a PR commit. |
| Dependency job passes but package is absent | Inspect the dependency diff for `workshop-lab/dependency/requirements.txt`, PyJWT, and the exact version. Empty discovery is incomplete, not a passing fixture exercise. Keep the threshold high. |
| Dependency review says unsupported/not ready, or its API returns 403 | Confirm dependency graph is enabled in **Settings > Advanced Security** and your account is permitted to use it. Wait up to five minutes, then rerun once. If it still fails, escalate with the run URL. This is availability/setup failure, not advisory detection; do not lower the threshold or enable a bypass. |
| Dependency repair still fails | Read the actual advisory and affected range. A newer advisory may require a kit update. Do not add allowlists or `warn-only`, and do not silently substitute an unverified version. |

## Secrets

Only use the fixture with documented nonfunctionality and recent route verification. Never authenticate with it. Repository push protection can behave differently for a value already detected in that repository; rehearse in fresh history.

For a blocked web edit, replace the value in the uncommitted buffer and retry. No local commit exists to amend. For one newest unpublished terminal commit, follow lesson 5's targeted `git add` and amend.

### More than one unpublished secret commit

1. Stop the timed exercise. Read every commit/path listed in the rejection and confirm none of those commits was published or shared.
2. Save nonsecret work independently. Do not create a published backup branch containing the value.
3. Find the earliest affected commit with `git log --oneline`. Replace `EARLIEST` below with its hash:

   ```bash
   git rebase -i EARLIEST^
   ```

4. Mark every affected commit as `edit`. At each pause, remove the value, stage only the corrected file, run `git commit --amend --no-edit`, then `git rebase --continue`. Resolve conflicts carefully; a later commit can reintroduce the value.
5. Inspect all rewritten unpublished changes and push the clean branch normally. No force push is needed when the rejected branch was never published.

If the earliest commit is the root, the branch has shared history, or you are unsure about publication, stop and get help rather than applying this sequence blindly. For a real exposure, revoke/rotate first and follow the organization's incident process.

If the supplied fixture is not blocked, mark the result incomplete. Do not bypass, mint a real token, or claim a recording as your own live result.

## Rules and release

| Symptom | Check and recovery |
|---|---|
| Unexpected owner-review requirement | Inspect inherited `CODEOWNERS`, repository rulesets, and organization rules. Lab 1 removes upstream names and does not enable required owner review. Do not override an organization policy. |
| Passing checks but merge blocked | Inspect missing/stale checks, up-to-date requirement, unresolved reviews, and code-scanning policy. Update the branch normally and wait for the new revision. Do not bypass. |
| Release workflow guard fails | Inspect its specific error. The workflow must be on `main`; `workshop-demo` must already have a reviewer and exactly one branch-only `main` rule. API failures are blocking, not success. |
| No approval wait | Stop. Verify environment name/settings before treating the run as an approved release. |
| Solo approval unavailable | Add your account as required reviewer and leave self-review prevention off for this training environment. Keep administrator bypass disabled. |
| Waiting release is stale | Cancel it. Run current `main` and wait for its prerequisites. An old green run cannot validate a new SHA. |
| Receipt expired or upload failed | Record expiration/failure. A rerun creates a new attempt and needs its own prerequisites/approval; do not reconstruct a receipt and call it the original. |

## Checkpoint

Record the failing step, exact error, revision/run URL, kit version, and safe next action. Exclude tokens and private data. If the issue remains unresolved, its outcome stays incomplete.

## Resources

[Required checks troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [blocked-push repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line), and [environment protection](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

| [Previous: dependency maintenance](3-maintain-dependencies.md) | [Next: annotated solutions](../solutions/README.md) |
|:---|---:|
