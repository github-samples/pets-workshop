# 2. Approve a cloud-free release

| [Previous: merge policy](1-enforce-merge-policy.md) | [Next: dependency maintenance](3-maintain-dependencies.md) |
|:---|---:|

## Why it matters

The shelter needs to know which revision passed its checks and who approved its release. This lab records that decision in a small artifact. It does not deploy an application or provision cloud resources.

## 1. Configure the environment first

Complete Lab 1 and confirm your safe change is on `main`. Do not install the third workflow until this environment exists:

1. Open **Settings > Environments > New environment**. Name it exactly `workshop-demo`.
2. Enable **Required reviewers**, add your own account, and save the protection rule.
3. Leave **Prevent self-review** off for solo practice. You can approve your own simulated release. This is a training accommodation, not production separation of duties.
4. Disable **Allow administrators to bypass configured protection rules**. Do not use a bypass if a run is blocked.
5. Under **Deployment branches and tags**, select **Selected branches and tags**. Add one **Branch** rule with the exact name `main`. Do not add a tag rule, wildcard, or **Protected branches only**.
6. Reopen the environment and verify the reviewer and branch rule. Add no environment secrets, cloud credentials, or variables.

Public repositories support required reviewers on GitHub Free. If your account cannot configure them, keep the lab incomplete and follow [troubleshooting](troubleshooting.md).

## 2. Review and install the third workflow

1. Create branch `exercise/release-simulation` from current prepared `main`.
2. Copy the complete [release starter](../starter/release-simulation.yml) to `.github/workflows/release-simulation.yml`. The setup helper intentionally does not install this file.
3. Inspect its behavior before committing:

   | Control | What the supplied workflow does |
   |---|---|
   | Trigger | Push to `main` or manual dispatch; guard rejects other refs/events |
   | Policy | Reads the existing environment; fails if approval/main-only rules are missing |
   | Revision | Checks out exact `github.sha` for both release prerequisites |
   | Prerequisites | Repeats API tests and client build; failed, skipped, or cancelled jobs cannot release |
   | Approval | `release` waits for `workshop-demo`; current main/policy checked again afterward |
   | Permissions | `contents: read`; no cloud identity, PR-target trigger, or persisted checkout credential |
   | Output | `receipt.json`, its SHA-256 file, and artifact identity in the summary; retention three days |

4. Open a PR titled **Add the reviewed release simulation** against your own `main`. Review the YAML yourself; the solo ruleset does not require a second approver.
5. Wait for the existing required PR checks and CodeQL policy to pass. The release workflow itself does not run for PR events and is not a new required PR check.
6. Merge this workflow PR normally. Record the resulting `main` SHA.

For terminal users, after creating/editing on that branch:

```bash
git add -- .github/workflows/release-simulation.yml
git diff --cached
git commit -m "Add reviewed cloud-free release simulation"
git push -u origin exercise/release-simulation
```

## 3. Inspect, approve, and verify

1. Open **Actions > Release simulation** and the run for that merge SHA. The push trigger should start it. For recovery, choose **Run workflow > main**; the manual route repeats the same guard and tests.
2. Confirm `guard`, `release-api-tests`, and `release-client-build` all succeed. Their revision must match this run, not an earlier green PR revision. CodeQL/dependency policy was enforced at merge; these release jobs repeat functional checks on the merged revision.
3. The `release` job should wait for review. Record that waiting state before approval. If it runs without waiting, stop: the approval control was not demonstrated.
4. Select **Review deployments**, choose `workshop-demo`, inspect the revision, add an approval comment, and select **Approve and deploy**. No application is deployed despite the UI wording.
5. Open the completed run summary. Record the commit SHA, run URL and attempt, artifact ID and URL, `receipt.json` checksum, and archive digest.
6. Download the small receipt artifact before its three-day expiration. Open `receipt.json` and confirm `kind` is `workshop-simulation-no-deployment`, its SHA is the run's `main` SHA, and the prerequisite names are correct.

The checksum printed for `receipt.json` is different from the uploaded archive's digest. To check the file locally after unzipping, use one available command:

```bash
# macOS
shasum -a 256 -c receipt.sha256

# Linux or Git Bash
sha256sum -c receipt.sha256
```

Without local tools, inspect the file and compare the receipt fields with the summary; mark independent checksum verification unperformed. This does not require installing a hashing tool.

## 4. Handle failures without bypassing

| Result | Action |
|---|---|
| Guard fails on environment policy or an API error | Fix the stated setting/access problem, then run current `main` again. A missing response never means approval exists. |
| API test/build fails | Diagnose it in a new PR, get required checks passing, and merge the repair. Do not approve a release from the failed run. |
| A prerequisite is skipped or cancelled | No receipt should be produced. Rerun the full workflow when ready; do not turn the release condition into `always()` alone. |
| Waiting job belongs to an older SHA | Cancel it and run current `main`. The post-approval guard also rejects stale revisions. |
| Manual run selects a branch or tag | Guard must fail. Select `main`; do not remove the branch guard. |
| Approval cannot be given by the solo owner | Check reviewer membership and self-review prevention. Do not bypass the environment. |
| Upload fails after approval | Treat the run as failed. No complete release receipt exists until upload and summary both succeed. |

For a safe negative check, use **Run workflow** with a non-`main` branch that contains this unchanged workflow. Confirm the guard rejects it and there is no receipt. Do not weaken the workflow to create a negative example. Cancel an in-progress run if you need to stop work; it does not become a successful release.

## 5. Clean up

Save the public evidence links and any receipt you need. Artifacts expire after three days; you may delete an individual artifact earlier through its run page. Do not delete other people's runs or repositories.

If you want no further simulations, disable **Release simulation** from its Actions menu, or remove only `.github/workflows/release-simulation.yml` through a reviewed PR. Cancel pending runs first. Keep the `workshop-demo` environment until no workflow references it; deleting it while the workflow remains can cause automatic recreation without your rules. Keep the core workflows and useful security settings enabled.

## Checkpoint

Your own run shows successful same-revision prerequisites, a waiting approval, approval by the configured reviewer, and a completed receipt. Record the negative non-main result separately. [Evidence examples](../fixtures/evidence-examples.md) show the expected fields without inventing run IDs.

## Resources

[Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments), [review deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

| [Previous: merge policy](1-enforce-merge-policy.md) | [Next: dependency maintenance](3-maintain-dependencies.md) |
|:---|---:|
