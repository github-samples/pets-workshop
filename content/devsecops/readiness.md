# Readiness register

## Why it matters

Published instructions, local tests, and a successful author run answer different questions. This register separates them so the event's promise matches the evidence.

Kit 0.1.2 is a **Codespaces-first prerelease**. The complete editing/setup route is authored, but actual Codespaces and representative learner rehearsals remain required before calling it event-ready. The two core workflow files, 75-minute core, and optional status of the job-token exercise are unchanged.

## Codespaces rehearsal status

The authoring environment's existing GitHub CLI identity was `frye`. The read-only `GET /user/codespaces` preflight returned HTTP 403 with `Must have admin rights to Repository`; the CLI also reported that the request needs the missing `codespace` OAuth scope. An authenticated browser control path was unavailable: the canvas exposed actions requiring a page handle that its open operation did not supply.

No extra auth consent, broader credential, PAT, billing change, or alternate access mechanism was used to force the test. Payer, available allowance, machine options, creation, configured Git authentication, workflow-file pushes, blocked secret push, and stop/resume persistence were therefore **not observed in Codespaces**. The exact authorized fresh repository was absent when inspected; it was not created after this access blocker. No codespace was created, so there is no codespace ID or stopped/running resource to report and no rehearsal compute/storage resource was started.

This does not mean the learner's account lacks Codespaces. It limits what this authoring session could verify. The primary guide follows official Codespaces documentation; earlier local-terminal and native Linux results below are not substituted for live Codespaces evidence. [Structured rehearsal status](fixtures/codespaces-rehearsal.json) records the same boundary.

## Observed in the authorized rehearsal repository

Only `frye/pets-devsecops-rehearsal` was used for these GitHub checks. It was created from the original Pets template. No upstream settings, workflows, branches, or PRs were changed.

| Check | Evidence and scope |
|---|---|
| Original-source compatibility | Upstream/local source both `d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a`; helper accepted independent template history |
| Two core workflows | Installed by the actual helper, committed before exercise branches |
| Baseline API/build | [CI run 35672436993](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672436993), successful on `2bce2ba54f8879e7fd58bcab03ca450ae4855a77` |
| Baseline CodeQL | [Initial run](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672218502), [alert 1](https://github.com/frye/pets-devsecops-rehearsal/security/code-scanning/1): high `py/flask-debug`, `app/server/app.py:83` |
| Harmless starter PR | [Working PR](https://github.com/frye/pets-devsecops-rehearsal/pull/6); harmless dependency-review [run attempt 2](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672600492/attempts/2) passed |
| Code fix and test | [Fix analysis](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672748825) succeeded; query of open alerts for `refs/pull/6/merge` returned none at fix `80d6a4bad2a0bc37ab83deb213276a6aacd638cd` |
| Dependency discovery/failure | [Training PR](https://github.com/frye/pets-devsecops-rehearsal/pull/7), [failed run attempt 2](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672637386/attempts/2): real manifest/PyJWT 2.3.0 and high advisories |
| Dependency repair | [Passing review](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35672886819) at `a5827834bab893ea529e5bab5727bf0c32fbf438`, PyJWT 2.14.0 |
| Merge enforcement | Active [ruleset](https://github.com/frye/pets-devsecops-rehearsal/rules/23797186), no bypass; PR7 reported `BLOCKED` while advisory check failed, then `CLEAN` after repair; closed without merge |
| Safe application merge | PR6 merged at `120020d58297ba0c9027d9419f264f79fd07b17b` only after required checks and policy passed |
| Default-branch closure | Alert 1 reported `fixed` after the safe merge; `fixed_at` was `2026-09-22T00:42:27Z` |
| Secret terminal route | Official inactive fixture rejected with GH013; amended unpublished commit and clean retry succeeded. [Provenance and redacted evidence](fixtures/secret-validation.md) |
| Environment setup | `workshop-demo` created before release workflow; reviewer configured, self-review allowed, admin bypass false, one branch-only `main` policy |
| Approved release | [Workflow PR](https://github.com/frye/pets-devsecops-rehearsal/pull/8) passed required checks before merge. [Run 35673125582](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35673125582) validated `de046227a52580e22f5834ff7ba907a60c7b3860`, waited for review, then succeeded after configured reviewer approval through REST |
| Receipt | Artifact `10672032391`, 586 bytes, three-day retention; downloaded receipt checksum verified. [Preserved receipt and provenance](fixtures/recorded-release/metadata.json) |
| Non-main manual rejection | [Run 35673266895](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35673266895): guard failed, API/build/release skipped, zero artifacts |
| Manual main prerequisites | [Run 35673404998](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35673404998): guard/API/build succeeded, then waited for approval with zero artifacts; deliberately cancelled without approval |
| Dependency maintenance | [PR9](https://github.com/frye/pets-devsecops-rehearsal/pull/9) merged after checks at `c8f99979360a20d3063a592416b85cf0e1c1bfb3`; [pip update job](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35673510830) and [Actions update job](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35673511009) accepted the shipped configuration and succeeded |
| Independent CodeQL policy check | Never-merged [author PR11](https://github.com/frye/pets-devsecops-rehearsal/pull/11) restored only the original debug setting in an isolated negative fixture. Functional/dependency checks passed, analysis jobs succeeded, but [CodeQL reported one new high finding](https://github.com/frye/pets-devsecops-rehearsal/runs/106575303204) and merge was blocked. Safe restoration `0f7b42e` passed every check and became eligible; the PR was closed without merge. No server ran; the mock assertion was temporarily adjusted only to isolate the scanning policy |
| Native helper and fetch tests | [Author-only run 35674158519](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35674158519) passed 20 helper cases plus three fetch/manifest cases on both standard Ubuntu 24.04 and Windows 2022 Git Bash runners. The temporary author workflow was not merged or shipped as an active workflow |

The initial dependency-review attempts failed with an unsupported/not-ready message rather than an advisory. The comparison API returned 403 and an alert-enable request returned 422. A later bounded recheck returned the actual manifest/advisories, and reruns produced the results above. The cause of the transient state was not established; the kit does not claim that the alert-enable request fixed it.

The inherited dependency baseline also produced Dependabot alerts, including high and critical findings. Dependency review evaluates new PR introductions; passing this workshop's checks does not clear existing alerts or make the sample production-ready. Those existing packages were not silently upgraded as part of this track.

## Local evidence

The 50-test suite covers helper/fetch, startup, release, and 17 targeted job-token cases. The fetch regression now replaces `FETCH_HEAD` after verifying the companion SHA and confirms that extraction still uses the saved commit, preserves learner history, and installs only the two core workflows. It is a disposable local test, not a Codespaces session.

The token cases check exact denial classification, separate permissions, main-only execution, bot issue identity, unexpected success, failed cleanup, and recovery messages after an ambiguous network failure. They do not simulate a forcibly terminated runner. Shell syntax, actionlint, four unchanged inert workflows, Markdown links/anchors, command/config snippets, route consistency, and kit inventory are checked separately.

The existing three API tests pass. In a disposable source copy, the added startup test fails against the original debug setting and all four tests pass after the one-line fix. The unchanged Astro client builds with Node 24. The upstream application and other workshop tracks retain their original behavior.

Local execution used macOS Bash; the native runner checks above cover Linux and Git Bash too. They exposed a real CRLF fingerprint-path issue, reproduced locally and fixed by stripping only the terminal carriage return before the existing validations. A separate regression checks CRLF-manifest read-only/apply behavior and still rejects application drift. Kit-scoped `.gitattributes` keeps distributed text LF; no global Git configuration was changed. Automated platform checks are not a human learner walkthrough.

## Optional job-token exercise

[Rehearsal PR12](https://github.com/frye/pets-devsecops-rehearsal/pull/12) passed the existing required checks and CodeQL policy before merging at `93c56ca7002a4ad2bf1aa982ffbaab293f74a9c2`. No ruleset bypass or repository-default workflow-permission change was used.

[Main run 35688557307](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35688557307) reported `Issues: read` for `deny-issue-write`. The actual POST returned the expected HTTP 403 integration-permission message with remaining rate-limit budget. The separate `allow-issue-write` job reported `Issues: write`, received HTTP 201, and verified the returned `github-actions[bot]` creator/type. [Training issue 13](https://github.com/frye/pets-devsecops-rehearsal/issues/13) was created at `2026-09-22T04:53:11Z` and closed by the cleanup step at `2026-09-22T04:53:12Z`; the issue API independently confirmed its closed state and matching run marker.

[Non-main run 35688654756](https://github.com/frye/pets-devsecops-rehearsal/actions/runs/35688654756) failed the ref guard before API access and skipped the allowed job. The repository's matching training-issue list contained only the one closed main-run issue. The unrelated release run triggered by the workflow merge was cancelled without approval. [Recorded identity evidence](fixtures/token-permissions-evidence.json) preserves these results without token values.

The optional workflow uses only inline Python on a standard hosted runner. Core workflows, installer, application, and runtime selections are unchanged in v0.1.2. The companion fetch instructions now archive a captured, verified commit; the local regression covers background ref replacement. Existing native helper evidence is retained without claiming native tests proved Codespaces-specific behavior.

This is GitHub API permission evidence, not cloud federation evidence. No OIDC ID token was requested and no Azure/AWS login or provider role was configured. The OIDC guidance was checked against official documentation, including immutable subject claims. The optional workflow's browser presentation and a fresh self-service human walkthrough remain unobserved.

## Remaining event go/no-go gates

| Gate | Required evidence |
|---|---|
| Actual Codespaces primary route | An authorized smallest suitable space with known payer/allowance: existing clone, verified companion fetch, helper setup, workflow-file commit/push with configured auth, code/dependency changes, actual blocked secret push/repair, stop/resume and persistent kit; stop it after rehearsal |
| Fresh learner Step 0 | A reader follows account selection, original template creation, own-repo codespace startup and complete prework without hidden setup or presenter intervention |
| File-editor fallback | Actual blocked GitHub.com create/edit commit and corrected uncommitted retry in a fresh learner copy; official screenshots alone do not prove this route |
| Take-home independence | Readers resume the same codespace and complete post-event, partial, and fresh-copy paths using only the guides, including closed/merged PR recovery; record fallback use separately |
| Timing and room | Representative prepared learners, participant-owned laptops, one presenter and 1-2 helpers; measured core <=75 minutes without bypasses; venue network/power and turnout confirmed |
| Event-date drift | Recheck original-template fingerprints, action releases, advisories, supported secret pattern behavior, and fixture safety before delivery |

No Codespaces startup, UI action, or screenshot is claimed from the blocked access attempt. Earlier CLI/REST observations remain labeled as such. No real learner timing has been measured.

## Checkpoint

Retain this prerelease status until the missing evidence is recorded. A recorded demonstration can support teaching during a service delay but leaves the participant's required individual checkpoint incomplete.

## Resources

[GitHub template behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [dependency graph setup](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/enable-dependency-graph), and [GitHub Skills fixture source](https://github.com/skills/introduction-to-secret-scanning/blob/77045e069f9deda2beba27990d65899c4ee4b221/.github/steps/3-enable-push-protection.md).
