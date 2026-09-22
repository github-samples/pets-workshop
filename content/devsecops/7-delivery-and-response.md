# 7. Approve a simulated release and plan a response

| [Previous: merge policy](6-merge-policy.md) | [Next: closing](8-wrap-up.md) |
|:---|---:|

Budget: 8 minutes. Facilitator demonstration and discussion. No participant environment, third workflow, or cloud account is required now.

## Why it matters

Release approval is a decision about a particular revision and its evidence. A traceable receipt helps the shelter identify what was approved when a later advisory appears.

## Explore together

1. Inspect the presenter's **Release simulation** run. Its guard accepts only current `main`, requires an existing `workshop-demo` environment with a reviewer and one branch-only `main` policy, and fails on missing or unreadable policy.
2. Watch `release-api-tests` and `release-client-build` validate the same `github.sha`. Manual dispatch repeats these prerequisites; it does not reuse a green run from another commit.
3. While they run, discuss the [incident card](fixtures/incident-card.md). Assign an owner and choose which evidence you need before patching or reverting.
4. Inspect the waiting `release` job, then approve the `workshop-demo` deployment. Solo self-approval is allowed in this training environment; it is not separation of duties.
5. Open the run summary. Match the commit SHA and run attempt to the artifact ID, `receipt.json` checksum, and uploaded archive digest. The artifact contains only a simulation receipt, expires after three days, and deploys nothing.

The release job checks current `main` again after approval. A stale run fails; cancel it and run the new revision. A concurrent branch change after the final check is still possible: this small simulation is not an atomic production promotion system.

If a prerequisite is delayed or fails, leave release blocked. Use discussion time or a clearly labeled earlier receipt with its real source links. Never approve a failed revision or remove protection to meet the timebox.

## Checkpoint

Identify the approved revision and one response action. Your personal release configuration and receipt are outcomes of [take-home Lab 2](take-home/2-approve-a-release.md), not of watching this demonstration.

## Resources

[Secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use), [deployment environments and approvals](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments), and [NIST SSDF response practices](https://csrc.nist.gov/projects/ssdf).

| [Previous: merge policy](6-merge-policy.md) | [Next: closing](8-wrap-up.md) |
|:---|---:|
