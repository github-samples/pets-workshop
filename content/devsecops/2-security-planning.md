# 2. Plan the shelter's security checks

| [Previous: baseline](1-devops-baseline.md) | [Next: code scanning](3-code-scanning.md) |
|:---|---:|

Budget: 6 minutes. Your team is preparing a shelter release.

## Why it matters

A short threat model helps the team choose controls for specific failure scenarios and decide who handles their results.

```mermaid
flowchart LR
    Browser --> Astro["Astro frontend"]
    Astro --> Flask["Flask API"]
    Flask --> SQLite["SQLite sample shelter data"]
    Contributor --> Repository
    Repository --> Actions["Actions: tests and build"]
    Actions --> Review["Merge policy"]
    Review --> Approval["Approved release simulation"]
```

This is a delivery sketch, not a claim that the workshop deploys a hosted service. The sample application has no learner authentication or customer-PII subsystem to add to the model.

## Try it

1. Discuss four questions: What are we building? What could go wrong? What will we do about it? How will we know?
2. Complete the blank control and owner cells below in your PR description or `workshop-notes.md`. Owners can be roles; do not publish private staff information.
3. Agree on an observable acceptance result for each row.

| Asset and risk | Control to complete | Owner to assign | Acceptance result |
|---|---|---|---|
| API process: direct startup enables a debugger | Safe default plus regression test | ___ | `debug=False` asserted and targeted CodeQL finding removed |
| Dependency change: introduces a vulnerable package | ___ | Maintainer | High-severity introduction fails review; repaired version passes |
| Repository history: contains a credential | Repository push protection and exposure response | ___ | Verified nonfunctional fixture blocked; clean retry succeeds |

## Checkpoint

You have three risk/control/owner rows and can explain what evidence would satisfy each one. The secret row remains incomplete until a live block and clean retry are observed; writing the criterion does not satisfy it.

## Resources

[OWASP threat modeling](https://owasp.org/www-community/Threat_Modeling) describes the four questions. [NIST SSDF](https://csrc.nist.gov/projects/ssdf) covers responsibilities across development and response.

| [Previous: baseline](1-devops-baseline.md) | [Next: code scanning](3-code-scanning.md) |
|:---|---:|
