# 1. Configure and prove merge enforcement

| [Previous: resume](0-resume.md) | [Next: approve a release](2-approve-a-release.md) |
|:---|---:|

## Why it matters

Checks provide feedback; required checks prevent a merge that does not meet the policy. You will prove both a blocked and a repaired state without merging the training dependency.

## 1. Prepare the safe PR

1. Complete [Resume](0-resume.md) in your existing codespace. Your safe PR must contain the startup fix and regression test, or a harmless note if that fix already reached `main`. After confirming the tree is clean, switch to that PR's branch; substitute `exercise/shelter-resume` if you created it during recovery:

   ```bash
   git status --short
   git switch exercise/shelter-change
   ```
2. In the Codespaces editor, edit `.github/CODEOWNERS` on the safe branch. Remove the inherited upstream owner line `* @scubaninja @geektrainer`. Keep a comment such as `# Training repository: no required code-owner review.` Do not assign strangers as reviewers. Save the file, then:

   ```bash
   git add -- .github/CODEOWNERS
   git diff --cached -- .github/CODEOWNERS
   git commit -m "Remove inherited owners from the learner copy"
   git push
   ```

3. On GitHub.com, wait for that revision's `api-tests`, `client-build`, `dependency-review`, and CodeQL analysis. Record the check names exactly as displayed. Workflow titles such as `CI` are not the required job names.

## 2. Create the ruleset

1. On your learner repository's GitHub website, open **Settings > Rules > Rulesets > New ruleset > New branch ruleset**.
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

1. In Codespaces, start with no unrelated changes and create a new isolated branch:

   ```bash
   git status --short
   git fetch origin
   git switch main
   git merge --ff-only origin/main
   git switch -c exercise/dependency-policy
   ```

   If reusing the live dependency branch instead, switch to it after preserving work and confirm it contains the current core workflows.
2. Add or replace only the exercise manifest using the fetched [before fixture](../fixtures/dependency-before.txt):

   ```bash
   mkdir -p workshop-lab/dependency
   cp ../pets-devsecops-kit-v0.1.2/fixtures/dependency-before.txt workshop-lab/dependency/requirements.txt
   ```

   Open the file in the editor and confirm:

   ```text
   PyJWT==2.3.0
   ```

3. Commit and push the fixture, then open the PR on GitHub titled **Training only: prove dependency policy; do not merge**:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Prove the dependency merge policy"
   git push -u origin exercise/dependency-policy
   ```

   If reusing a different branch, push that branch instead. Never install the lab manifest in Codespaces or merge it.
4. Wait for the dependency diff to show this manifest and package, then the high-severity failed check. Confirm GitHub's merge control is blocked specifically by required `dependency-review`. Record the failed run, PR revision, ruleset, and blocked-merge evidence.
5. In the Codespaces editor, replace the one line using the fetched kit's [repair](../fixtures/dependency-after.txt):

   ```text
   PyJWT==2.14.0
   ```

6. Save, commit, and push the repair:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Repair dependency policy training fixture"
   git push
   ```

   If `main` advanced, update the branch normally and inspect the new Actions checks on GitHub. Confirm all required checks pass and the PR is eligible for merge.
7. **Do not click Merge.** Record the eligible state, then close this training PR without merging it. Delete its remote branch only if you no longer need it; the PR/run evidence remains available.

A missing/queued check is a policy block, but it is not the dependency-failure proof. An empty dependency diff is not a successful discovery result. Keep either case incomplete until diagnosed.

## 4. Merge only safe application work

1. Return to the safe working PR. Confirm its changed files contain no dependency-training directory and no secret fixture.
2. Inspect the startup fix/test and CODEOWNERS change. Confirm all required checks pass on the latest revision and the intended CodeQL finding is absent from its results.
3. Use GitHub's normal merge control. Do not bypass rules. Save the merge commit SHA and resulting `main` CI run.
4. After default-branch analysis completes, confirm the debug alert is closed/fixed. A green PR check alone does not prove the default-branch alert has closed.

## Checkpoint

Save your active ruleset settings, blocked dependency merge, repaired eligibility, closed-unmerged fixture PR, safe merge SHA, and post-merge analysis. The [evidence checklist](../evidence.md) keeps those results separate.

When pausing, push safe intended work and stop the codespace explicitly. If Codespaces is unavailable, [local Git](../0-setup.md#fallback-a-local-vs-code-and-git) uses these commands; the [file-editor fallback](../0-setup.md#fallback-b-github-file-editor) commits the same edits on the same named branches. Rules, merges, and results stay on GitHub for every route.

## Resources

[Create branch rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository), [code-scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection), and [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

| [Previous: resume](0-resume.md) | [Next: approve a release](2-approve-a-release.md) |
|:---|---:|
