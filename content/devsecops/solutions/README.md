# Annotated solutions

| [Previous: troubleshooting](../take-home/troubleshooting.md) | [Next: evidence checklist](../evidence.md) |
|:---|---:|

## Why it matters

A solution should explain the intended behavior and how to check it. Copying a fix without its evidence leaves the original question unanswered.

Use the Codespaces editor and integrated terminal for the learner edits. Copy material from the fetched `../pets-devsecops-kit-v0.1.2` sibling, save it, review the exact staged files, then commit and push to the intended exercise branch. Inspect checks and configure repository controls on GitHub.com. Local Git and file editing are labeled fallbacks in [Step 0](../0-setup.md); do not clone the app again inside Codespaces.

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
| Editing environment | Own learner codespace, default image, existing checkout and sibling kit under `/workspaces` | No app install, extra clone, or required devcontainer; builds/tests stay in Actions |
| Check names | `api-tests`, `client-build`, `dependency-review` | These are job names, not workflow titles |
| Core/release permissions | `contents: read`, no `pull_request_target`, no stored checkout credential | PR code receives no deployment privilege |
| Dependency threshold | `high`, all scopes, `warn-only: false` | The training failure must block |
| Ruleset | Active on `main`, empty bypass, required PR/checks, CodeQL high, zero peer approvals | Solo-compatible enforcement |
| CODEOWNERS | Remove upstream usernames in the learner copy; no required owner review | Do not assign people who do not maintain this copy |
| Environment | `workshop-demo`, reviewer is learner, self-review allowed, admin bypass off, one branch rule `main` | Demonstrates approval without a second account |
| Release | [release-simulation.yml](../starter/release-simulation.yml), exact SHA, successful prerequisites, approval | Manual dispatch cannot skip checks |
| Dependabot | [Complete config](dependabot.yml): npm, pip, Actions | Covers all three dependency sources without promising immediate PRs |
| Optional identity exercise | [token-permissions.yml](../starter/token-permissions.yml): manual `main` only; separate `issues: read` and `issues: write` jobs; no checkout | Demonstrates least privilege without changing repository defaults or core setup |

## Optional workload-identity proof

In [take-home Lab 4](../take-home/4-workload-identity.md), the first job is green only when the GitHub API returns the precise non-rate-limited integration-permission HTTP 403. A generic 403, missing Issues feature, authentication failure, or network error does not prove the intended control.

The second job receives a different installation token with `issues: write`. HTTP 201, the actual `github-actions[bot]` creator, and a closed matching issue prove the allowed operation and cleanup. The user who initiated the run is not the bot identity. Each job's cleanup runs even after a failed proof, but does not override that failure; interruption may still require manual closure of the exact recorded issue.

The developer `GITHUB_TOKEN` configured in Codespaces is not that Actions job token. Do not print either or execute the workflow proof in the Codespaces terminal. Copy and review the YAML there, then dispatch it on GitHub.

No `contents: write`, broad grant, or `id-token: write` is needed. OIDC ID-token requests and provider-issued cloud permissions are separate concepts explained in the guide, not actions performed by this workflow.

## Secret repair

Remove the verified nonfunctional value; never choose bypass. A blocked web edit has no created commit, so correct the buffer and retry. A blocked terminal push may include local commits: remove the value from every affected unpublished commit, not just the final tree. The [secret lesson](../5-secrets.md) and [recovery guide](../take-home/troubleshooting.md#more-than-one-unpublished-secret-commit) distinguish those cases.

Codespaces is the primary route for the blocked push and repair. Earlier local-terminal evidence does not establish Codespaces authentication. Save and push safe work, then explicitly stop the codespace after practice; stopped storage still counts, and deletion requires preserving needed work first.

## Checkpoint

Compare your diff and settings with these answers, then verify the corresponding run/rejection/approval evidence. Matching text alone does not prove a remote control worked.

## Resources

[CodeQL Flask debug rule](https://codeql.github.com/codeql-query-help/python/py-flask-debug/), [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), and [secure Actions use](https://docs.github.com/en/actions/reference/security/secure-use).

| [Previous: troubleshooting](../take-home/troubleshooting.md) | [Next: evidence checklist](../evidence.md) |
|:---|---:|
