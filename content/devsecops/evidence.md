# Your workshop evidence

| [Previous: annotated solutions](solutions/README.md) | [Next: take-home index](take-home/README.md) |
|:---|---:|

## Why it matters

Evidence links let you return to the exact revision and result. Record only public workshop data; exclude credentials, fixture values, and private screenshots.

Write your repository URL, kit version, date, and route first: **Codespaces primary**, local Git fallback, or file-editor fallback. Keep only a nonsecret codespace identifier for your own resume record; do not share tokens or connection secrets. Use these status words consistently:

| Status | Meaning |
|---|---|
| Live complete | You performed the action and observed the required result |
| Pending | The required service result has not arrived |
| Incomplete | The action failed, was unavailable, or lacked required evidence |
| Recorded demonstration | A labeled prior result from an identified repository/run |
| Observed demonstration | You watched the presenter; it is not your own configuration |
| Not attempted | You have not started the exercise |

## Individual live work

| Outcome | Evidence to record | Status |
|---|---|---|
| Prework | Repository, kit version, baseline CI run, open harmless PR | ___ |
| Codespaces readiness | Correct existing clone/origin, allowed payer/usage, startup, verified companion fetch and workflow push; or named fallback | ___ |
| Threat model | Three risk/control/owner rows in notes or PR description | ___ |
| Code remediation | Fix/test commit, passing CI, latest PR CodeQL result without targeted finding | ___ |
| Dependency failure | Manifest visible in dependency diff, high advisory/version, failed run | ___ |
| Dependency repair | Repaired commit and passing run; PR remains unmerged | ___ |
| Secret protection | Codespaces/local blocked push plus unpublished repair, or fallback web blocked commit; redacted evidence and clean retry | ___ |

## Demonstrations

| Outcome | Record |
|---|---|
| Merge policy | Rule that blocked the presenter's PR; live or recorded source |
| Release approval | Demonstrated commit/run/artifact/checksum; live or recorded source |
| Response | Affected revision/dependency, owner, chosen next action |

## Optional take-home completion

| Outcome | Evidence to record | Status |
|---|---|---|
| Enforced merge | Active ruleset, failed required dependency check and blocked merge, repaired eligibility | ___ |
| Safe merge | Working PR merge SHA, successful `main` checks, default-branch alert closure | ___ |
| Approved release | Same-SHA prerequisites, waiting approval, approver, receipt and artifact ID | ___ |
| Negative release | Non-main dispatch rejected with no receipt | ___ |
| Maintenance | Merged npm/pip/Actions configuration and accepted update job/configuration | ___ |
| Optional job-token identity | Run/revision; separate job grants; exact integration403 with rate budget; HTTP201, bot creator, issue URL and closed state | ___ |
| Optional identity ref guard | Non-main manual attempt rejected before any API mutation; allowed job skipped | ___ |
| Cleanup | Fixture PRs not merged, pending runs cancelled, receipt saved before expiry | ___ |
| Codespaces lifecycle | Safe work pushed, sibling kit retained under `/workspaces`, observed stop/resume, final space explicitly stopped | ___ |

## Checkpoint

Leave any unanswered row incomplete. A recording, absent dependency diff, successful analysis with findings, or later deletion of a committed secret does not satisfy the corresponding live criterion.

The optional identity exercise is not another core requirement. Its OIDC references are further reading: GitHub issue authorization does not demonstrate Azure/AWS login or cloud resource access.

An earlier local-terminal test is not Codespaces evidence. Record unobserved startup, configured authentication, workflow pushes, secret repair, or persistence as incomplete rather than borrowing another route's result.

## Resources

[Review workflow runs](https://docs.github.com/en/actions/how-tos/monitor-workflows/using-workflow-run-logs) and [review dependency changes](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review).

| [Previous: annotated solutions](solutions/README.md) | [Next: take-home index](take-home/README.md) |
|:---|---:|
