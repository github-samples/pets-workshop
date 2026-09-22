# 1. Inspect the DevOps baseline

| [Previous: setup](0-setup.md) | [Next: security planning](2-security-planning.md) |
|:---|---:|

Budget: 7 minutes. The shelter's PR has a green build. What does that result cover?

Keep the same Codespaces editor and terminal open for the participant work. Inspect checks on GitHub.com; the commands in their logs execute in Actions, not in your codespace.

## Why it matters

Functional checks catch regressions in behavior they exercise. The existing API tests mock database queries and never start the server, so a passing run says nothing about startup debug mode.

## Try it

1. Open your prepared `exercise/shelter-change` PR. Check that the latest revision reports `api-tests`, `client-build`, and `dependency-review`.
2. Open `api-tests` and find `python -m unittest test_app -v`, run from `app/server`. Open `client-build` and find `npm ci` followed by `npm run build`.
3. In the Codespaces editor, inspect `.github/workflows/ci.yml` and `app/server/test_app.py`. Identify what the mocks replace and which paths the tests exercise. The existing Playwright suite provides optional browser coverage outside this workshop's required checks.
4. In your notes, sketch `change -> PR -> checks -> merge`. Add two questions the current functional tests do not answer.

## Who authenticates the workflow?

Each job receives its own `GITHUB_TOKEN`, an installation access token for GitHub's Actions App scoped to this repository. It is not your PAT and expires when the job finishes or reaches its effective maximum lifetime. In the CI file, `permissions: contents: read` limits what this identity can do; other configurable permissions are none unless explicitly granted.

Codespaces also configures a developer credential, sometimes named `GITHUB_TOKEN`. That is a different identity context used for your repository work. Never print either token or run the optional workflow's proof code in the terminal using developer credentials.

Inspect **Set up job > GITHUB_TOKEN Permissions** alongside the YAML. Explain why checkout needs repository-content read access and why tests do not need issue-write or source-write permission. Compare each grant with what the job actually needs.

The [optional workload-identity lab](take-home/4-workload-identity.md) lets you observe denied issue creation, then a separate job that creates and closes a training issue. It needs no cloud account or personal token and stays outside this lesson's seven-minute budget. Its [OIDC guide](take-home/4-workload-identity.md#beyond-the-repository-oidc) points to provider trust and short-lived cloud credentials for later study.

## Checkpoint

Record the green baseline run, the job's repository read permission, and two blind spots, such as debug startup and known dependency vulnerabilities. A useful note is: "API assertions passed at this revision; startup configuration was not tested." Do not describe that as a complete security assessment.

## Resources

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration) explains automated feedback. The existing [Pets testing lesson](https://github.com/github-samples/pets-workshop/blob/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a/content/github-actions/3-running-tests.md) covers a broader pipeline; use Node 24 for this track, not its older Node 20 example.

[GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) documents the job identity, repository scope, and lifetime. [Authentication examples](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) show job-level permission grants.

| [Previous: setup](0-setup.md) | [Next: security planning](2-security-planning.md) |
|:---|---:|
