# 0. Resume without losing your work

| [Previous: take-home index](README.md) | [Next: merge policy](1-enforce-merge-policy.md) |
|:---|---:|

## Why it matters

Your repository may have changed since the event. Establish its current state before adding rules or trying to recreate an exercise.

## Inspect your state

1. Confirm you own the public learner repository and can administer it. Check both core files on remote `main`: `.github/workflows/ci.yml` and `.github/workflows/dependency-review.yml`.
2. Open your working PR and dependency-training PR, if they exist. Record their branch names, state, latest commit, and checks. Inspect the actual file contents as well as old run links.
3. Confirm CodeQL default setup, dependency graph, secret scanning, and repository push protection are enabled. Check the current kit's [readiness register](../readiness.md) for any unresolved exercise blocker.
4. Before any local branch switch, inspect `git status --short`. Commit your work to its intended branch or move it yourself; these labs never reset or stash it for you.

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

A required workflow must exist in the branch you use. With the web route, create new exercise branches from current `main`. If an existing PR is behind, use **Update branch** when available and review the resulting checks; conflicts need a deliberate manual resolution.

With Git, the following updates local `main` only if it can move forward without a merge. Substitute a different working branch only if your PR uses it:

```bash
git status --short
git fetch origin
git switch main
git merge --ff-only origin/main
git switch exercise/shelter-change
git merge main
```

Start only with a clean working tree. If the fast-forward or merge fails, stop and inspect the conflict; do not force it. These commands use the learner's own origin, never companion or upstream history.

## Checkpoint

You have an open safe PR, working core checks on its current revision, and a separate unmerged dependency exercise. Any missing live outcome remains labeled incomplete; it does not prevent learning about the later controls as long as their own prerequisites pass.

## Resources

[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) and [keeping a pull request up to date](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch).

| [Previous: take-home index](README.md) | [Next: merge policy](1-enforce-merge-policy.md) |
|:---|---:|
