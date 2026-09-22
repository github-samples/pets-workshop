# 0. Resume without losing your work

| [Previous: take-home index](README.md) | [Next: merge policy](1-enforce-merge-policy.md) |
|:---|---:|

## Why it matters

Your repository may have changed since the event. Establish its current state before adding rules or trying to recreate an exercise.

## Reopen the same codespace

1. At [github.com/codespaces](https://github.com/codespaces), find the space for **your learner repository** and reopen it. Check access, payer, and remaining usage; do not change spending settings to resume. Do not create a new space merely because the old one is stopped.
2. Wait for initialization and open **Terminal > New Terminal**. Inspect the existing checkout:

   ```bash
   repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root"
   pwd
   git remote get-url origin
   git branch --show-current
   git status --short
   test -f ../pets-devsecops-kit-v0.1.2/workshop-kit.json
   ```

3. Confirm the root is under `/workspaces` and origin names your learner repository. Saved workspace files, including the sibling kit, persist across stop/start and rebuild. A newly created replacement space will not contain the previous space's unpushed work or kit.
4. If the v0.1.2 kit is missing or you only have v0.1.1, follow [Step 0's fetch/extract section](../0-setup.md#04-fetch-the-companion-beside-the-existing-checkout). Do not rerun initial installation against an already remediated application or overwrite an old kit. Keep all versions outside the app checkout.

If quota prevents resuming, follow [the recovery guide](troubleshooting.md#codespaces-access-and-recovery) and preserve work before using a fallback. Do not delete a space to resolve an authentication or quota error.

## Inspect your state

1. Confirm you own the public learner repository and can administer it. Check both core files on remote `main`: `.github/workflows/ci.yml` and `.github/workflows/dependency-review.yml`.
2. Open your working PR and dependency-training PR, if they exist. Record their branch names, state, latest commit, and checks. Inspect the actual file contents as well as old run links.
3. Confirm CodeQL default setup, dependency graph, secret scanning, and repository push protection are enabled. Check the current kit's [readiness register](../readiness.md) for any unresolved exercise blocker.
4. Before a branch switch in the Codespaces terminal, inspect `git status --short`. Commit your work to its intended branch or preserve it separately; these labs never reset or stash it for you.

| State | Safe next action |
|---|---|
| Live code/dependency work complete; working PR open | Keep it open. Save evidence and continue to Lab 1. |
| Code fix submitted, results pending or failed | Inspect the latest revision and finish [lesson 3](../3-code-scanning.md). Do not count an older green revision. |
| Dependency failure or repair missing | Resume [lesson 4](../4-dependencies.md). Verify discovery before claiming a passing result. |
| Working PR closed without merge | Reopen it if GitHub permits and the branch still exists. Otherwise create `exercise/shelter-resume` from current prepared `main`, apply only missing safe edits, and open a new PR. |
| Working PR already merged | Confirm `debug=False`, the regression test, and post-merge analysis on `main`. Create `exercise/shelter-resume` with a harmless note change for the required-PR exercise. Do not restore debug mode to recreate the old finding. |
| Dependency PR closed or branch gone | Create a new isolated `exercise/dependency-policy` branch from current prepared `main` during Lab 1. Never merge the lab manifest. |
| Fresh template copy | Complete [all of Step 0](../0-setup.md), then lessons 1-4. Keep secret protection marked incomplete if the fixture is unavailable. Return here afterward. |
| App files intentionally changed since setup | Do not rerun the strict helper or overwrite them. Compare workflows manually with this kit, validate compatibility, and preserve the changes. |

The helper checks the original application's fingerprints for initial setup. It can therefore refuse a correctly remediated repository; use the manual comparison above for later updates.

## Refresh a branch safely

A required workflow must exist in the branch you use. In the same codespace, update your local `main` from your learner origin before starting new take-home branches. For an existing working PR, the commands below merge the updated `main` into its branch.

The fast-forward command refuses divergent local `main`. Substitute your actual working branch if it differs from `exercise/shelter-change`. If the working branch is gone or its PR was already merged, run only through the fast-forward of `main`, then use the new-branch sequence below; do not run the last two lines:

```bash
git status --short
git fetch origin
git switch main
git merge --ff-only origin/main
git switch exercise/shelter-change
git merge main
```

Start only with a clean working tree. If the fast-forward or merge fails, stop and inspect the conflict; do not force it. These commands use the learner's own origin, never companion or upstream history.

To recreate the working PR after updating `main`, create a new branch with `git switch -c exercise/shelter-resume`, edit `workshop-notes.md` in the Codespaces editor with a harmless resume note, and save:

```bash
git add -- workshop-notes.md
git diff --cached -- workshop-notes.md
git commit -m "Resume the shelter workshop"
git push -u origin exercise/shelter-resume
```

Open the new PR on GitHub against your own `main`. Apply only missing code/test edits, using this branch name in later instructions. Never restore the unsafe debug setting just to recreate prework.

For the file-editor fallback, create new branches from current remote `main` and use **Update branch** for an existing PR when available. Resolve conflicts deliberately. The local Git fallback uses the same terminal commands without Codespaces lifecycle assumptions.

## Checkpoint

You have an open safe PR, working core checks on its current revision, and a separate unmerged dependency exercise. Any missing live outcome remains labeled incomplete; it does not prevent learning about the later controls as long as their own prerequisites pass.

When pausing, verify safe commits are pushed, then explicitly stop this codespace. Closing the tab is not a stop; delete only after preserving needed work and evidence.

## Resources

[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) and [keeping a pull request up to date](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch).

| [Previous: take-home index](README.md) | [Next: merge policy](1-enforce-merge-policy.md) |
|:---|---:|
