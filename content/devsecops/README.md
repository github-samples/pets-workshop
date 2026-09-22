# DevSecOps: from a green build to a safer release

| [Workshop selection](https://github.com/github-samples/pets-workshop/blob/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a/content/README.md) | [Next: setup](0-setup.md) |
|:---|---:|

You're volunteering at the dog shelter. Its Flask API and Astro website pass their functional tests. Now you need to check what happens when a change leaves the debugger enabled, introduces a vulnerable package, or includes a credential.

You'll fix code, review a dependency change, and practice secret protection in your own public repository. The presenter demonstrates merge policy and a cloud-free release. The [take-home labs](take-home/README.md) include the instructions and files to perform those two exercises yourself afterward.

> [!IMPORTANT]
> Kit **0.1.0** is a prerelease for review and rehearsal. The [readiness register](readiness.md) records actual checks and remaining gaps, including fresh browser-only walkthroughs and human timing. Do not treat publication as approval to promise every attendee a completed 75-minute core.

## What you need

Bring a laptop with internet access. Your GitHub.com account must be able to create and administer a public learner repository, run standard GitHub-hosted Actions, and configure its security settings. Use only the shelter's public sample data.

GitHub Free supports the public-repository features used here, subject to account and organization policies. No local Python, Node.js, Docker, Azure account, Codespaces, Copilot subscription, second reviewer, GitHub CLI, or pasted personal access token is required. Git and VS Code are optional; the narrated route uses GitHub.com's file editor. A [terminal route](0-setup.md#terminal-route) reaches the same baseline.

Complete [Step 0](0-setup.md) before the event. The opening eight minutes only verify readiness.

## Agenda

These are design budgets. No representative learner rehearsal has established the timing.

| Lesson | Event minutes | Budget | Format |
|---|---:|---:|---|
| [0. Setup checkpoint](0-setup.md) | 00-08 | 8 | Verify prework |
| [1. DevOps baseline](1-devops-baseline.md) | 08-15 | 7 | Shared discussion |
| [2. Security planning](2-security-planning.md) | 15-21 | 6 | Shared planning |
| [3. Code scanning](3-code-scanning.md) | 21-38 | 17 | Individual fix and test |
| [4. Dependencies](4-dependencies.md) | 38-53 | 15 | Individual failure and repair |
| [5. Secrets](5-secrets.md) | 53-65 | 12 | Individual block and clean retry |
| [6. Merge policy](6-merge-policy.md) | 65-75 | 10 | Facilitator demonstration |
| [7. Delivery and response](7-delivery-and-response.md) | 75-83 | 8 | Facilitator demonstration |
| [8. Closing](8-wrap-up.md) | 83-90 | 7 | Evidence and questions |

The core totals 75 minutes; startup and closing bring the event to 90. Playwright, cloud deployment, and participant settings changes for lessons 6-7 are outside that core.

## Using this kit

Create a learner repository from the [original Pets template](https://github.com/github-samples/pets-workshop), then fetch the versioned kit from [frye/pets-devsecops-workshop](https://github.com/frye/pets-devsecops-workshop/tree/v0.1.0). [Step 0](0-setup.md) shows how to extract the fetched kit outside your learner clone without adding a remote or merging history. The browser route copies the same version's raw files. The optional helper installs only two core workflows.

The companion is not an application template. If the original template changes incompatibly, the organizer must refresh and retest the companion kit. The [versioned ZIP](https://github.com/frye/pets-devsecops-workshop/releases/tag/v0.1.0) is an optional alternative to Git fetch.

The kit works as a local folder: all lesson, starter, solution, and take-home links are relative. External links to existing Pets material use the inspected source revision. Files introduced by this track are never linked to an upstream location where they do not exist.

| Your next task | Guide |
|---|---|
| Start from no setup | [Step 0](0-setup.md) |
| Return after the event or recover partial work | [Resume](take-home/0-resume.md) |
| Find exact edits and explanations | [Solutions](solutions/README.md) |
| Track personal results | [Evidence checklist](evidence.md) |
| Run the event or build the companion archive | [Facilitator guide](facilitator.md) |
| Diagnose a failed step | [Troubleshooting](take-home/troubleshooting.md) |
| Review pins, advisories, and limitations | [Technical sources](sources.md) |

## Why it matters

The shelter needs evidence about both functionality and risk. Each lesson identifies the control, the person responsible, and the result that would justify moving forward. A pending check stays pending; watching the presenter's successful run does not complete your individual exercise.

## Optional primers

[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) explains the PR cycle. [What is DevOps?](https://learn.microsoft.com/en-us/devops/what-is-devops) introduces the delivery process. [NIST's Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) connects development to vulnerability response.

| [Workshop selection](https://github.com/github-samples/pets-workshop/blob/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a/content/README.md) | [Next: setup](0-setup.md) |
|:---|---:|
