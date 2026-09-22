# Secret fixture provenance and validation

## Why it matters

A plausible-looking token may not be blocked. A real credential is never an acceptable way to make a training example reliable.

## Supplied source

[secret-training.txt](secret-training.txt) contains the delimiter-masked training value from GitHub's official [Introduction to secret scanning, step 3](https://github.com/skills/introduction-to-secret-scanning/blob/77045e069f9deda2beba27990d65899c4ee4b221/.github/steps/3-enable-push-protection.md), pinned at `77045e069f9deda2beba27990d65899c4ee4b221`.

That source explicitly calls the value **inactive** and shows removing `<REMOVE_ME>` before a blocked web commit. Its [license](SKILLS-LICENSE) permits reuse. We rely on that primary-source inactive designation; the value was never used to authenticate or tested against a credential-validation service.

Keep `<REMOVE_ME>` in the distributed kit, screenshots, and any committed handout. Remove it only in the isolated exercise edit immediately before the attempted protected commit/push. Do not follow the source course's later bypass activity or its earlier instruction to disable protection. This workshop always keeps protection enabled and repairs the rejected change.

## Observed authoring evidence

On 2026-09-22 UTC in the authorized fresh-original-template repository `frye/pets-devsecops-rehearsal`:

| Route/action | Actual result |
|---|---|
| Repository protection settings | Secret scanning and repository push protection enabled |
| Earlier local-terminal fixture push | Rejected with `GH013`, `GITHUB PUSH PROTECTION`, pattern `GitHub Personal Access Token`, path `secret-training.txt:1`, unpublished commit `28007175f0dc7ea3f0b7d1965d5b33bc66949491` |
| Earlier local-terminal repair | Only affected unpublished commit amended; clean [commit 5b63409](https://github.com/frye/pets-devsecops-rehearsal/commit/5b634090fa8e021f9322cfe87c789ae1d1e88f0c) pushed successfully with `TRAINING_VALUE_REMOVED` |
| Codespaces primary attempt | Not executed: authoring access failed before a codespace could be created. No Codespaces developer-authentication, blocked-push, or repair result is claimed |
| Bypass | Not used; the fixture-containing commit never reached the remote branch |
| Fresh web create/edit route in this kit | Not executed: no authenticated shared-browser page handle was available |

The official course supplies web-UI instructions/screenshots, but that is source evidence, not a fresh learner-copy rehearsal of this kit. Do not mark the latter complete. No secret value or bypass URL is included in the rejection excerpt.

## Before each event

1. Recheck the pinned source and inactive designation. If the fixture changes or its safety is uncertain, stop rather than inventing a substitute.
2. Use an explicitly authorized fresh learner copy with repository protection enabled. Confirm the value has not already been detected or bypassed there.
3. In the learner's existing codespace, perform the primary terminal attempt, record the actual secret-protection rejection, remove the value from every affected unpublished commit, and verify a clean normal push. Authentication/network failure is not secret detection. Never substitute the Codespaces developer token for this inactive fixture.
4. Independently perform the GitHub.com create/edit attempt. Confirm a blocked commit, correct the uncommitted edit, and record the successful retry. Do not substitute REST behavior for the UI route.
5. Record repository, date, kit version, source revision, route, redacted rejection, clean retry, and absence of bypass. Recheck on the event network and supported account type.

If either live route fails, report the limitation before the event and revisit the delivery promise. A labeled recording can support discussion but cannot satisfy every participant's required individual live block.

## Checkpoint and resources

The earlier local-terminal block/repair is observed. Actual Codespaces and fresh file-editor attempts remain separate readiness gates. See [supported patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns) and [web push protection](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-in-the-github-ui) for detection limits, including values already detected in a repository.
