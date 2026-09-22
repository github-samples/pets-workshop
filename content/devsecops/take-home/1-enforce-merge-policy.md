# 1. Configure and prove merge enforcement

| [Previous: resume](0-resume.md) | [Next: approve a release](2-approve-a-release.md) |
|:---|---:|

## Why it matters

Checks provide feedback; required checks prevent a merge that does not meet the policy. You will prove both a blocked and a repaired state without merging the training dependency.

## 1. Prepare the safe PR

1. Complete [Resume](0-resume.md). Your safe PR must contain the startup fix and regression test, or a harmless note if that fix already reached `main`.
2. In this learner copy, edit `.github/CODEOWNERS` on the safe PR. Remove the inherited upstream owner line `* @scubaninja @geektrainer`. Keep a comment such as `# Training repository: no required code-owner review.` Do not assign strangers as reviewers. You can replace it with your own handle later if you want ownership routing.
3. Wait for that revision's `api-tests`, `client-build`, `dependency-review`, and CodeQL analysis. Record the check names exactly as displayed. Workflow titles such as `CI` are not the required job names.

## 2. Create the ruleset

1. Open **Settings > Rules > Rulesets > New ruleset > New branch ruleset**.
2. Name it `workshop-main`, set **Enforcement status** to **Active**, and leave the bypass list empty.
3. Under **Target branches**, add an inclusion pattern for `main` only.
4. Enable **Require a pull request before merging**. Set required approvals to **0**. Leave code-owner review and last-push approval off for this solo lab. Do not require a second person.
5. Enable **Require status checks to pass**, add the observed checks below, and select **GitHub Actions** as their expected source where the UI allows it:

   ```text
   api-tests
   client-build
   dependency-review
   ```

6. Require the branch to be up to date before merging. Do not enable merge queue in this lab; these starters do not include a `merge_group` trigger.
7. Enable **Require code scanning results**. Add **CodeQL** and select **High or higher** for security alerts. If the UI also offers a general alert severity, select **Errors** and record it. This is separate from requiring a successful workflow.
8. Save the ruleset and reopen it to confirm its active state, `main` target, empty bypass list, and exact check names.

If a check is missing from the selector, make a harmless PR update or rerun its actual PR workflow first. Confirm the starter exists on both branches. Do not add a guessed name or disable the requirement to merge.

CodeQL merge protection primarily evaluates findings introduced in the PR's changes. Existing default-branch findings outside that diff and Dependabot PRs with default setup have documented limitations. The old debug alert may stay open until the safe fix merges; its existence alone does not prove this PR should be blocked.

## 3. Prove a safe dependency failure

1. From current prepared `main`, create `exercise/dependency-policy`. If reusing the live dependency branch, first confirm it has the current core workflows and no unrelated changes.
2. Add or replace `workshop-lab/dependency/requirements.txt` with the supplied [before fixture](../fixtures/dependency-before.txt):

   ```text
   PyJWT==2.3.0
   ```

3. Open a PR titled **Training only: prove dependency policy; do not merge**.
4. Wait for the dependency diff to show this manifest and package, then the high-severity failed check. Confirm GitHub's merge control is blocked specifically by required `dependency-review`. Record the failed run, PR revision, ruleset, and blocked-merge evidence.
5. Replace the one line with the [repair](../fixtures/dependency-after.txt):

   ```text
   PyJWT==2.14.0
   ```

6. Commit the repair. If `main` advanced, update the branch normally and rerun the checks. Confirm all required checks pass and the PR is eligible for merge.
7. **Do not click Merge.** Record the eligible state, then close this training PR without merging it. Delete its remote branch only if you no longer need it; the PR/run evidence remains available.

A missing/queued check is a policy block, but it is not the dependency-failure proof. An empty dependency diff is not a successful discovery result. Keep either case incomplete until diagnosed.

## 4. Merge only safe application work

1. Return to the safe working PR. Confirm its changed files contain no dependency-training directory and no secret fixture.
2. Inspect the startup fix/test and CODEOWNERS change. Confirm all required checks pass on the latest revision and the intended CodeQL finding is absent from its results.
3. Use GitHub's normal merge control. Do not bypass rules. Save the merge commit SHA and resulting `main` CI run.
4. After default-branch analysis completes, confirm the debug alert is closed/fixed. A green PR check alone does not prove the default-branch alert has closed.

## Checkpoint

Save your active ruleset settings, blocked dependency merge, repaired eligibility, closed-unmerged fixture PR, safe merge SHA, and post-merge analysis. The [evidence checklist](../evidence.md) keeps those results separate.

## Resources

[Create branch rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository), [code-scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection), and [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

| [Previous: resume](0-resume.md) | [Next: approve a release](2-approve-a-release.md) |
|:---|---:|
