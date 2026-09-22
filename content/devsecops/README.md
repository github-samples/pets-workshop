# DevSecOps: from a green build to a safer release

| [Workshop selection](https://github.com/github-samples/pets-workshop/blob/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a/content/README.md) | [Next: setup](0-setup.md) |
|:---|---:|

You're volunteering at the dog shelter. Its Flask API and Astro website pass their functional tests. Now you need to check what happens when a change leaves the debugger enabled, introduces a vulnerable package, or includes a credential.

You'll fix code, review a dependency change, and practice secret protection in your own public repository. The presenter demonstrates merge policy and a cloud-free release. The [take-home labs](take-home/README.md) include the instructions and files to perform those two exercises yourself afterward.

> [!IMPORTANT]
> Kit **0.1.2** is a Codespaces-first prerelease. Actual Codespaces and human walkthroughs remain pending; the [readiness register](readiness.md) records the access limitation and earlier terminal/Actions evidence separately.

## What you need

Bring a laptop with internet access. Your GitHub.com account must be able to create and administer a public learner repository, run standard GitHub-hosted Actions, configure its security settings, and use Codespaces with sufficient included usage or approved sponsorship. Use only the shelter's public sample data.

The primary route uses browser-based VS Code in **GitHub Codespaces**. Git and Bash are already available there; you do not clone the learner repository again or install the application. You need no laptop Python, Node.js, Docker, or Git installation, and no Azure account, Copilot subscription, second reviewer, or pasted PAT. Use the default image and smallest suitable permitted machine, normally two cores, for editing and Git.

Codespaces compute and storage have usage limits and a payer; public repositories do not provide unlimited free Codespaces. Check access, quota, and who pays before starting. Standard Actions usage is separate. If policy, quota, or connectivity prevents the primary route, use the documented [local Git](0-setup.md#fallback-a-local-vs-code-and-git) or [file-editor fallback](0-setup.md#fallback-b-github-file-editor).

Throughout these guides, **editor** and **terminal** mean the Codespaces editor and integrated Bash terminal unless labeled as a fallback. GitHub.com remains the place for PRs, settings, Actions dispatch/results, and approval. Application builds, tests, scans, and the optional token proof run in Actions, not Codespaces.

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

For optional practice afterward, [prove a workflow's GitHub API permissions](take-home/4-workload-identity.md) yourself: observe a denied request, then a separate narrowly authorized job and its closed training issue. The guide also points to OIDC for future cloud identity work. Neither extends core setup or replaces the secret-protection exercise.

## Using this kit

Create a learner repository from the [original Pets template](https://github.com/github-samples/pets-workshop), then open a codespace on **your copy's `main`**. From its existing checkout, fetch the versioned [companion kit](https://github.com/frye/pets-devsecops-workshop/tree/v0.1.2) into a sibling under `/workspaces`. [Step 0](0-setup.md) gives the full sequence. The helper installs only two core workflows, without adding a remote or merging histories.

The companion is not an application template. If the original template changes incompatibly, the organizer must refresh and retest the companion kit. The [versioned ZIP](https://github.com/frye/pets-devsecops-workshop/releases/tag/v0.1.2) is an alternative way to obtain the same material.

Reuse one codespace for the learner repository. Saving is not committing or pushing. Keep the sibling kit under `/workspaces`, preserve intended work on GitHub, and [stop the codespace explicitly](0-setup.md#010-stop-and-reuse-the-same-codespace) when finished; closing its tab does not stop compute. Stopped storage still counts toward usage. Keep forwarded ports private; no app hosting is added.

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
