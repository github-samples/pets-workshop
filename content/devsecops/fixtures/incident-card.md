# Incident card: an advisory after release

Use during the release demonstration while checks run. This is a fictional response scenario, not a claim that the shelter was exploited.

## Scenario

A new advisory affects a dependency used by a released revision. You have the release receipt, the manifest and lockfile at that SHA, and an owner who can review a patch. You do not yet know whether the vulnerable behavior is reachable in this application.

## Why it matters

New advisories may require a patch, a revert, or further investigation after the original checks passed.

## Discuss

1. Identify the dependency and affected range from the advisory. Compare them with the exact released revision rather than the current branch.
2. Assign an owner and decide how to assess reachability and potential impact. Separate known facts from questions.
3. Choose a patch or revert candidate. Name the tests, dependency review, and scan results needed before merge.
4. Decide who approves the replacement release and how to record its receipt. If this were a credential exposure, revocation/rotation and access review would come before source cleanup.

## Checkpoint

Record the owner, chosen next action, evidence still needed, and how you would identify the replacement revision. This workshop simulates the decision; it does not execute a production rollback.

## Resources

[NIST SSDF](https://csrc.nist.gov/projects/ssdf) includes responding to vulnerabilities, and [Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) supplies dependency context.
