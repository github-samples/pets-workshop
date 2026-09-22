# Annotated solutions

| [Previous: troubleshooting](../take-home/troubleshooting.md) | [Next: evidence checklist](../evidence.md) |
|:---|---:|

## Why it matters

A solution should explain the intended behavior and how to check it. Copying a fix without its evidence leaves the original question unanswered.

## Code fix and regression test

In `app/server/app.py`, the direct entry point becomes:

```python
if __name__ == '__main__':
    app.run(debug=False, port=5100) # Port 5100 to avoid macOS conflicts
```

Insert [startup-test.py.txt](startup-test.py.txt) inside `TestApp` in `app/server/test_app.py`. The existing `patch` import is reused. `runpy` exercises the actual direct entry point while `Flask.run` is mocked, so no server starts. An in-memory database avoids modifying the sample database. Setting `FLASK_DEBUG=1` makes the assertion meaningful: explicit `debug=False` must override it.

The original three API tests still pass. Adding only the new test to the original source produces one assertion failure; changing the startup line gives four passing tests. This local test result does not substitute for CodeQL analysis.

Keep `app/scripts/common.sh` unchanged. Its intentional local debug setting belongs to another route. For production, select a proper WSGI server and deployment configuration outside this workshop.

## Dependency repair

The isolated manifest changes from [PyJWT 2.3.0](../fixtures/dependency-before.txt) to [2.14.0](../fixtures/dependency-after.txt). The earlier version is affected by the documented high-severity advisory. The repair accounts for later advisories too; see [sources](../sources.md).

CI installs only `app/server/requirements.txt`. It must never install the exercise manifest. Confirm the PR diff recognizes the package, observe the actual failure, and then the repaired check. Close the exercise PR without merging it.

## Workflow and settings answers

| Surface | Expected configuration | Reason |
|---|---|---|
| Core files | [ci.yml](../starter/ci.yml), [dependency-review.yml](../starter/dependency-review.yml) on `main` before branches | Required checks must report on all exercise PRs |
| Check names | `api-tests`, `client-build`, `dependency-review` | These are job names, not workflow titles |
| Permissions | `contents: read`, no `pull_request_target`, no stored checkout credential | PR code receives no deployment privilege |
| Dependency threshold | `high`, all scopes, `warn-only: false` | The training failure must block |
| Ruleset | Active on `main`, empty bypass, required PR/checks, CodeQL high, zero peer approvals | Solo-compatible enforcement |
| CODEOWNERS | Remove upstream usernames in the learner copy; no required owner review | Do not assign people who do not maintain this copy |
| Environment | `workshop-demo`, reviewer is learner, self-review allowed, admin bypass off, one branch rule `main` | Demonstrates approval without a second account |
| Release | [release-simulation.yml](../starter/release-simulation.yml), exact SHA, successful prerequisites, approval | Manual dispatch cannot skip checks |
| Dependabot | [Complete config](dependabot.yml): npm, pip, Actions | Covers all three dependency sources without promising immediate PRs |

## Secret repair

Remove the verified nonfunctional value; never choose bypass. A blocked web edit has no created commit, so correct the buffer and retry. A blocked terminal push may include local commits: remove the value from every affected unpublished commit, not just the final tree. The [secret lesson](../5-secrets.md) and [recovery guide](../take-home/troubleshooting.md#more-than-one-unpublished-secret-commit) distinguish those cases.

## Checkpoint

Compare your diff and settings with these answers, then verify the corresponding run/rejection/approval evidence. Matching text alone does not prove a remote control worked.

## Resources

[CodeQL Flask debug rule](https://codeql.github.com/codeql-query-help/python/py-flask-debug/), [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), and [secure Actions use](https://docs.github.com/en/actions/reference/security/secure-use).

| [Previous: troubleshooting](../take-home/troubleshooting.md) | [Next: evidence checklist](../evidence.md) |
|:---|---:|
