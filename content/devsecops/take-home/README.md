# Continue in your own repository

| [Previous: closing](../8-wrap-up.md) | [Next: resume](0-resume.md) |
|:---|---:|

These labs turn the live merge/release demonstrations into individual practice. All instructions and starter files ship with this kit; completing them after the event is optional.

## Why it matters

Configuring a rule is only part of the job. You also need to see a safe failure, repair it, and identify the revision the control allowed.

Use the same eligible GitHub.com account, public learner repository, and **existing codespace**, subject to remaining usage or approved sponsorship. Reopen it at [github.com/codespaces](https://github.com/codespaces) rather than creating one per lab. No Azure account, new payment method, second reviewer, laptop runtime, or PAT is required. Respect employer and organization policies.

Copy and edit files in the Codespaces editor, and run Git in its integrated terminal. Handle PRs, settings, workflow dispatch, results, and approvals on GitHub.com. Tests, builds, scans, and the optional token proof execute in Actions. Keep the fetched kit beside the app under `/workspaces`; [Resume](0-resume.md) handles a stopped space, missing kit, or an earlier kit version.

## Choose a starting point

1. Read [Resume](0-resume.md), even if you completed the live work. It handles closed or merged PRs and partially completed exercises without discarding changes.
2. Follow [Lab 1: enforce merge policy](1-enforce-merge-policy.md) to configure a solo-compatible ruleset, prove a dependency block, and merge only safe application work.
3. Follow [Lab 2: approve a release](2-approve-a-release.md) to configure the environment before installing the third workflow, approve a validated revision, and inspect your receipt.
4. Follow [Lab 3: maintain dependencies](3-maintain-dependencies.md) to add pip/Actions update coverage and prepare for future update PRs.
5. Optionally follow [Lab 4: workload identity](4-workload-identity.md) to prove a denied GitHub API operation, a narrowly authorized job, and cleanup of its bot-created issue. It can be done after Step 0 without completing the release lab. The final section links to OIDC cloud-identity guidance; no cloud setup is required or claimed.

[Troubleshooting](troubleshooting.md), [annotated solutions](../solutions/README.md), and [the evidence checklist](../evidence.md) are shared references. The [readiness register](../readiness.md) distinguishes executed checks from remaining publication and rehearsal work.

If Codespaces is unavailable, use the [local Git](../0-setup.md#fallback-a-local-vs-code-and-git) or [file-editor fallback](../0-setup.md#fallback-b-github-file-editor) after preserving existing work. Record the route used. Before leaving any lab, save/push safe work and explicitly stop the codespace; stopped storage still counts.

## Checkpoint

Your take-home record should show your own enforced block/repair and approved receipt. A presenter's recording does not count as your configuration or run.

## Resources

[Repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) and [deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

| [Previous: closing](../8-wrap-up.md) | [Next: resume](0-resume.md) |
|:---|---:|
