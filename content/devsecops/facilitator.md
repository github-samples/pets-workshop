# Facilitator guide

| [Overview](README.md) | [Readiness register](readiness.md) |
|:---|---:|

## Why it matters

Up to 90 participant-owned laptops with one presenter and 1-2 helpers leave little room for live account repair. Prework and a single narrated route are part of the delivery plan.

## Before announcing the event

1. Use only the [original Pets template](https://github.com/github-samples/pets-workshop) for learner applications. Supply all customization through the versioned [companion repository](https://github.com/frye/pets-devsecops-workshop). The companion is a kit, not an application template.
2. Resolve every mandatory [readiness gate](readiness.md). Label source inspection and local tests separately from live GitHub results. A prerelease can support review, but it must not imply event readiness.
3. Recheck upstream fingerprints. If they drift, refresh and rehearse the companion against the original template. Do not switch attendees to a derived template.
4. Rehearse the actual Codespaces Step 0: access/payer/quota, original template copy, default-image startup, existing clone, companion fetch, two-workflow commit/push, security checks, and stop/resume with the kit still present. Test local Git and file-editor fallbacks separately. Earlier native Linux tests do not prove Codespaces authentication or persistence.
5. Rehearse with representative prepared learners and managed/personal laptops on the venue network. Record wall-clock editing, Actions latency, help requests, and every outcome. The arithmetic `8 + 75 + 7 = 90` is not timing evidence.

## Prework and staffing

Collect public repository, starter-PR, baseline-run URLs and kit version through existing event communications. Also ask whether Codespaces startup, companion fetch, and workflow push succeeded and whether the learner knows how to reopen and stop that space. Record a fallback explicitly. Helpers mark readiness before the event; do not collect tokens or private connection details, or require another service signup.

Narrate **Codespaces**, using the browser-based VS Code editor and integrated terminal. Keep the local Git and file-editor fallback references available for helpers rather than repeating every route. Assign the 1-2 helpers to tables or zones, prioritizing access/startup, Git problems, and the three individual exercises. At maximum capacity, a helper may cover 45-90 learners; revisit capacity if advance readiness is insufficient.

Confirm power, Wi-Fi, GitHub sign-in, the Codespaces editor/terminal and reconnection, and Actions access on representative personal/company-managed laptops. Check allowed quota or sponsorship before startup; do not change billing or machine size to force access. Use one smallest suitable codespace per learner repo, normally two cores, and no required custom devcontainer or app install. Neither a partner's run nor the presenter's repo completes another attendee's checkpoint.

## Prepare the two demonstrations

Use a separate, explicitly authorized facilitator repository. Never change participant settings for them.

1. Complete Step 0 and the code/dependency exercises there.
2. Use [take-home Lab 1](take-home/1-enforce-merge-policy.md) to configure rules, remove inherited owner names, and prepare a separate dependency PR with real failure and repair evidence.
3. Configure `workshop-demo` before installing [release-simulation.yml](starter/release-simulation.yml). Follow [Lab 2](take-home/2-approve-a-release.md), including main-only policy, solo approval, exact-SHA checks, negative test, and receipt inspection.
4. Keep separate safe application and dependency-training PRs. During the demonstration, merge only the safe one; close the fixture PR without merging.
5. Save labeled recordings/transcripts only from actual runs, with source URLs, revision, date, and kit version. If no recording exists, say so. [Expected-result examples](fixtures/evidence-examples.md) are not recordings.

## Run the room

| Event minute | Action |
|---:|---|
| 00-08 | Verify prework and resume the existing codespace; triage small remaining issues |
| 08-15 | Baseline and functional blind spots |
| 15-21 | Three-row threat model |
| 21-38 | Individual code fix/test; start scans |
| 38-53 | Callback to code results; dependency failure then repair |
| 53-65 | Individual secret-protection attempt and clean retry |
| 65-75 | Merge-policy demonstration; helpers revisit pending individual results |
| 75-83 | Release demonstration and incident card |
| 83-90 | Closing, honest evidence, take-home resume point |

After a four-minute wait, continue with the next independent activity and revisit the result at its callback. This is a facilitation threshold, not an Actions service promise. Do not repair a dependency before its initial failure is observed and then count the cycle as complete.

At minute 80, stop starting new troubleshooting/edit cycles. At minute 83, begin closing regardless of queues. Keep missing outcomes pending/incomplete. Never bypass secret protection, required checks, code-scanning policy, or approval to finish on time.

At closing, have learners save and push intended safe work and explicitly stop their own codespace. Closing a tab does not stop compute; stopped storage still counts. Keep forwarded ports private. Preserve needed work and evidence before deletion, and reopen the same space for take-home.

## Optional identity practice

During lesson 1's existing seven minutes, identify the job's GitHub App installation identity and read-only scope alongside the CI commands. Point to [the self-service workload-identity lab](take-home/4-workload-identity.md) for later practice. Offer its two-job permission exercise as optional take-home or a separately scheduled follow-along. Do not add a fourth required individual outcome to the 75-minute core; keep the secret exercise and all timeboxes unchanged.

Learners copy/edit the optional workflow in Codespaces and install it through a reviewed PR, not the setup helper. Its jobs execute only in Actions. Do not run the proof script with the developer `GITHUB_TOKEN` configured in Codespaces or print either credential. No cloud account, new app, PAT, or laptop runtime is required; OIDC remains provider-specific reading, not a claimed cloud test.

## Build and publish the companion

From the Pets source worktree, maintainers can validate and build the entire kit:

```bash
python3 -m unittest discover -s content/devsecops/tests -v
python3 content/devsecops/scripts/validate-kit.py
bash -n content/devsecops/scripts/prepare-devsecops.sh
actionlint content/devsecops/starter/ci.yml content/devsecops/starter/dependency-review.yml content/devsecops/starter/release-simulation.yml content/devsecops/starter/token-permissions.yml
python3 content/devsecops/scripts/build-kit.py --refresh-manifest --source-repo . --output-dir /path/to/kit-output
python3 content/devsecops/scripts/build-kit.py --output-dir /path/to/second-output
```

Use an isolated validation environment with Flask dependencies and PyYAML. The tests require access to the Pets source; when running from an extracted companion, set `PETS_SOURCE_REPO` to that checkout. These tools are author requirements, not attendee prerequisites.

For the author test suite on Windows, select the Git Bash executable explicitly before invoking Python. This avoids Python selecting the unrelated Windows Subsystem for Linux launcher:

```bash
export WORKSHOP_BASH="$(cygpath -w "$BASH")"
```

Run that command in Git Bash only. The learner's helper invocation already runs in their chosen Bash terminal.

The builder verifies the file inventory and emits a deterministic ZIP and SHA-256 sidecar. `--refresh-manifest` is an explicit authoring operation; it reads the pinned source commit for fingerprints and the original license. Compare archive hashes from the two builds. Output stays outside the source kit.

Publish the **contents of `content/devsecops/` at the companion root**, without application code, a surrounding `content/devsecops` directory, or active `.github/workflows`. Keep starter workflows inert. Use a new immutable version tag for each reviewed update. The archive, guides, source commit, and release body must agree on the version.

The builder can also generate planned links with `--publication-repo OWNER/REPO --publication-ref FULL_SHA`; it does not push, upload, or claim those links exist. Only the authorized companion owner publishes. Never push this worktree to `github-samples/pets-workshop`.

## Checkpoint

The complete live and take-home kit ships together, links and fetch commands work, and the readiness register distinguishes what is observed from what still needs a human/browser rehearsal. Preserve that distinction in the event invitation.

## Resources

[GitHub template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [Git archive](https://git-scm.com/docs/git-archive), and [Actions usage](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

[Codespaces creation](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), and [stop/start](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace) support the primary route.
