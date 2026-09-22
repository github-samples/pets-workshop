# 4. Prove what a workflow's identity can do

| [Previous: dependency maintenance](3-maintain-dependencies.md) | [Next: troubleshooting](troubleshooting.md) |
|:---|---:|

This optional exercise is outside the 75-minute core. Use the same public learner repository and GitHub.com account. You need no cloud account, PAT, app registration, Copilot subscription, or local tool installation. You will test GitHub API authorization, not Azure or AWS authentication.

## Why it matters

The shelter wants automation to create an issue without being able to change application code. You will observe a denied request and a separately authorized request, then confirm that the training issue was closed.

GitHub creates a distinct `GITHUB_TOKEN` for each job. It is an installation access token for the GitHub App installed when Actions is enabled, scoped to the repository containing the workflow. It is not the triggering person's PAT. It expires when the job finishes or reaches its effective maximum lifetime; these jobs also have five-minute execution timeouts. The workflow can use the token through `github.token` without you creating or copying it.

## 1. Check readiness

1. Complete [Step 0](../0-setup.md), or follow [Resume](0-resume.md) if returning to an existing learner copy. You need working PR checks and permission to merge a reviewed workflow.
2. Confirm **Issues** is available in your repository. If it is disabled, the repository owner can enable it under **Settings > General > Features > Issues**, if policy allows. Do not change another repository or work around organization policy.
3. Keep your current repository-default workflow permissions unchanged. This exercise specifies permission grants per job.
4. Open the v0.1.1 [token-permissions.yml starter](../starter/token-permissions.yml), or its [version-pinned raw file](https://raw.githubusercontent.com/frye/pets-devsecops-workshop/v0.1.1/starter/token-permissions.yml). Read it before installing it.

You can do this lab independently of the release/environment and dependency-maintenance labs. The setup helper still installs only the two core workflows; it will not install this optional file.

## 2. Review and add the workflow

1. From current `main`, prepare a change for a new `exercise/token-permissions` branch. In the web editor, select **Add file > Create new file**, name it `.github/workflows/token-permissions.yml`, and copy the entire starter.
2. Select **Commit changes**, choose a new branch named `exercise/token-permissions`, and open a PR against your own `main`.
3. Inspect these boundaries in the diff:

   | Setting | Expected behavior |
   |---|---|
   | Trigger | Only `workflow_dispatch`, with no user inputs |
   | Ref guard | Both proof and cleanup reject any ref other than `refs/heads/main` before an API call |
   | Workflow permissions | Empty default grant; no `contents: write`, `write-all`, or `id-token: write` |
   | First job | `deny-issue-write` has only `issues: read` |
   | Second job | `allow-issue-write` needs a successful first job and has only `issues: write` |
   | Execution | No checkout or third-party actions; fixed API requests use Python already on the standard hosted runner |
   | Cleanup | Each job's `always()` step can close only the recorded issue whose title, body marker, and bot creator match that run |

4. Review the PR yourself. Wait for `api-tests`, `client-build`, `dependency-review`, and any configured CodeQL merge policy to pass on its latest revision. Merge normally, without bypassing rules. This optional workflow does not run on PRs and is not another required PR check.
5. Confirm the file is on remote `main`. Keep the original core workflows unchanged.

If you installed the release simulation in Lab 2, this merge also starts its normal release run. You can cancel that specific run if you are not practicing release approval now. It is separate from the token exercise; do not approve it automatically or cancel someone else's run.

If using terminal Git, start from clean, up-to-date `main`, run `git switch -c exercise/token-permissions`, copy the starter to the path above, then:

```bash
git add -- .github/workflows/token-permissions.yml
git diff --cached
git commit -m "Add optional workflow identity exercise"
git push -u origin exercise/token-permissions
```

Open and review the PR in GitHub as described above. Python runs only on the hosted runner, so neither Python nor GitHub CLI is a laptop prerequisite.

## 3. Run once and inspect both job identities

1. Open **Actions > Token permissions > Run workflow**. Select `main` and start one run.
2. Open `deny-issue-write`. In **Set up job**, inspect the reported `GITHUB_TOKEN Permissions`: issue access should be read-only. GitHub also provides the installation's implicit metadata access; unspecified configurable permissions are set to none.
3. Open **Prove job-scoped issue permission**. It first checks that the repository is reachable, unarchived, and has Issues enabled. The attempted issue creation must return **HTTP 403**, the exact message **Resource not accessible by integration**, and a nonzero rate-limit budget with no retry delay.
4. Confirm the summary says **Expected denial confirmed**. This is a successful assertion of a denied operation, so a green first job is correct. A generic failed request is not the checkpoint.
5. Open `allow-issue-write` and compare its setup permissions. This is a separate job with a newly issued token that has `issues: write`; the first token was not upgraded in place.
6. Confirm creation returned **HTTP 201**, note the exact issue URL, and verify the reported creator is **github-actions[bot]**. The person who clicked **Run workflow** is the initiator, not the issue's authenticated bot actor.
7. Open **Close only this job's training issue** and confirm it reports **Confirmed closed**. Visit that exact issue and verify its **Closed** state, bot author, and body link back to your run.

The title is `[workshop-token-permissions] RUN_ID/ATTEMPT allow`. One allowed issue is created and immediately closed during a successful run; it remains visible as training evidence. No source code, default permissions, secrets, or cloud resources are changed.

The platform grant permits issue writes in this repository, not just one issue. The fixed request and run-marker checks keep this exercise's behavior narrower than the token's capability; they are workflow safeguards, not a per-issue permission grant.

Save the run URL and revision, both jobs' permission displays, the exact denial message, issue URL, bot creator, and confirmed closed state. The run summary is the receipt; no token or bearer header is printed. Do not add a debugging step that dumps environment variables or the full `github` context.

## 4. Handle failures and cleanup

| Result | What to do |
|---|---|
| First job reports 401, 404, 422, invalid JSON, or network failure | Mark the proof incomplete. Inspect the reported setup/service error. These are not the required authorization denial. |
| A 403 reports rate limiting, another message, or no usable rate-budget evidence | Stop and diagnose it. Wait for service/rate-limit recovery; do not count it as denied issue-write permission. |
| Repository preflight says Issues disabled or archived | Fix only your repository's intended setting within policy, then try again. No creation was attempted. |
| Read-only creation unexpectedly returns 201 | The proof deliberately fails and the allowed job does not run. The cleanup step attempts to close only that unexpected training issue; confirm its exact URL is closed before investigating permissions. |
| Allowed creation fails | Keep the proof incomplete. Check the job's actual permission display and account/organization policy. Do not enable `write-all`, `contents: write`, or more permissive repository defaults. |
| Cleanup fails or detects a changed issue | Open the exact **Created training issue** or **Cleanup target** URL in the log/summary. Verify the title, run marker, and bot author; use **Close issue** on only that issue. Do not bulk-close or delete issues. |
| Run is cancelled, times out, or loses its runner | Cleanup is best-effort under interruption. Inspect the exact recorded issue URL and close that issue manually if needed. Cleanup success cannot turn a failed or cancelled proof into a pass. |

If creation was interrupted before its number was returned, the summary includes an exact title and a **Recovery search** link. Search both open and closed issues, match the run URL/body marker and bot author, then record and close only the matching training issue. Do not rerun blindly: a server may have created an issue even if the client did not receive the response.

Each rerun has a new attempt number and may create one new training issue. Save your evidence first. If you no longer want this exercise available, disable **Token permissions** in its Actions menu or remove only `.github/workflows/token-permissions.yml` through a reviewed PR.

For an optional negative check, manually select the still-existing `exercise/token-permissions` branch containing the unchanged workflow. The first job must fail its main-only guard, the allowed job must be skipped, and no issue may be created. This is ref-guard evidence, not the permission-denial result.

## Beyond the repository: OIDC

`GITHUB_TOKEN` authorizes GitHub API requests within its repository permissions. For a future cloud deployment, GitHub's OIDC provider can issue an ID token asserting which workload is running. The cloud provider validates the token and its configured trust conditions, then issues its own short-lived access token with the permissions of the selected provider role.

Adding `id-token: write` allows a job to request an OIDC ID token. It does **not** grant cloud resource write access, replace a provider role, or authorize every workflow in a repository. Environment approval controls when a job can proceed; it is not cloud authentication. This kit does not add `id-token: write`, request an OIDC token, log in to a provider, or claim a cloud federation test.

For a separately approved cloud extension:

1. Start with [GitHub's OIDC overview](https://docs.github.com/en/actions/concepts/security/openid-connect) and [OIDC trust/claims reference](https://docs.github.com/en/actions/reference/security/oidc). Arrange the provider account and permissions needed to configure federation.
2. Bind provider trust to the intended repository identity, an allowed ref or protected environment, the expected audience, and the permitted workflow or reusable workflow where supported. Validate issuer and token lifetime as part of provider verification. Avoid broad wildcard subjects; supported claim conditions differ by provider.
3. Check the repository's **actual subject format**. GitHub.com repositories created after July 15, 2026 use ID-bearing immutable subjects; renames/transfers after that date also change the default. See [immutable subject claims](https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims). Do not blindly copy older `repo:ORG/REPO:ref:...` examples into a new learner repository's trust policy. Use the exact IDs, subject configuration, and audience for your intended workload without printing raw tokens.
4. Assign a least-privilege provider role and restrict the token-request permission to the job that needs it. Follow the official [Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure) or [AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) guide for the provider-specific exchange and trust conditions. AWS does not support arbitrary custom OIDC claims; use its documented mechanisms rather than assuming every GitHub claim is available as a condition.

Federation can avoid storing a long-lived cloud credential in GitHub. It still requires provider-side setup and uses short-lived credentials with explicitly assigned permissions.

## Checkpoint

You can identify the installation-token identity, show an actual expected denied operation, explain the separate narrowly authorized job, and link to its closed bot-created issue. You can also distinguish GitHub API authorization, OIDC identity assertions, and provider-issued access tokens. Cloud setup is further reading, not a completed lab outcome.

## Resources

[GITHUB_TOKEN scope and lifetime](https://docs.github.com/en/actions/concepts/security/github_token), [job-level authentication examples](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token), and [workflow permission semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions).

| [Previous: dependency maintenance](3-maintain-dependencies.md) | [Next: troubleshooting](troubleshooting.md) |
|:---|---:|
