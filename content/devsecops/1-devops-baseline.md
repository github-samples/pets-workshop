# 1. Inspect the DevOps baseline

| [Previous: setup](0-setup.md) | [Next: security planning](2-security-planning.md) |
|:---|---:|

Budget: 7 minutes. The shelter's PR has a green build. What does that result cover?

## Why it matters

Functional checks catch regressions in behavior they exercise. The existing API tests mock database queries and never start the server, so a passing run says nothing about startup debug mode.

## Try it

1. Open your prepared `exercise/shelter-change` PR. Check that the latest revision reports `api-tests`, `client-build`, and `dependency-review`.
2. Open `api-tests` and find `python -m unittest test_app -v`, run from `app/server`. Open `client-build` and find `npm ci` followed by `npm run build`.
3. Inspect `app/server/test_app.py`. Identify what the mocks replace and which paths the tests exercise. The existing Playwright suite provides optional browser coverage outside this workshop's required checks.
4. In your notes, sketch `change -> PR -> checks -> merge`. Add two questions the current functional tests do not answer.

## Checkpoint

Record the green baseline run and two blind spots, such as debug startup and known dependency vulnerabilities. A useful note is: "API assertions passed at this revision; startup configuration was not tested." Do not describe that as a complete security assessment.

## Resources

[Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration) explains automated feedback. The existing [Pets testing lesson](https://github.com/github-samples/pets-workshop/blob/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a/content/github-actions/3-running-tests.md) covers a broader pipeline; use Node 24 for this track, not its older Node 20 example.

| [Previous: setup](0-setup.md) | [Next: security planning](2-security-planning.md) |
|:---|---:|
