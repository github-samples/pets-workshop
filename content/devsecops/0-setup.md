# 0. Prepare your shelter repository in Codespaces

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|

## Why it matters

Complete setup before the event so you can spend the session on the security exercises. The first eight minutes verify readiness; they do not replace account setup, Codespaces startup, or initial scans.

> [!IMPORTANT]
> Use the [v0.1.2 companion kit](https://github.com/frye/pets-devsecops-workshop/tree/v0.1.2). Codespaces is primary; [local Git](#fallback-a-local-vs-code-and-git) and [GitHub file editing](#fallback-b-github-file-editor) are fallbacks. Actual Codespaces rehearsal remains pending; see the [readiness register](readiness.md).

Unless a step says otherwise, **editor** means browser-based VS Code in your codespace and **terminal** means its integrated Bash terminal. Run Git commands from your learner repository's root, in order, and stop at an error. GitHub's website remains the place for PRs, settings, Actions results, and approvals.

The primary flow is: **original Pets template -> your repository -> open its codespace -> fetch the companion and run the setup script -> normal VS Code/Git edits**. Codespaces has already cloned your repository; no second clone or application runtime setup is needed.

## 0.1 Choose an account and check usage

1. Sign in at [GitHub.com](https://github.com). Reuse an account that can create and administer a public repository, run Actions, and use Codespaces.
2. Follow employer policy on public training, personal accounts, and managed devices. Enterprise Managed Users cannot create public repositories; use an eligible personal account only if permitted. A GitHub Enterprise Server or GHE.com identity is not automatically a GitHub.com account.
3. If needed and permitted, use [GitHub signup](https://github.com/signup), select the free option, and verify an email you control. Do not reuse an email already verified for an Enterprise Managed User. Configure two-factor authentication and keep recovery information private.
4. Check the current username, Codespaces availability, and remaining compute/storage allowance in your account's **Billing and licensing > Usage** view. If an organization sponsors the codespace, confirm its policy and the payer shown during creation.
5. Use included usage or already approved sponsorship. A public repository does not make Codespaces unlimited or free of usage limits. Codespaces compute and storage are billed separately from standard Actions runners. Do not add a payment method, raise a budget, or change organization policy just to continue this lab.

If access, quota, policy, or connectivity prevents Codespaces use, choose a documented fallback. If neither fallback is permitted, arrange approved observation and mark individual outcomes incomplete. No PAT, Azure account, Copilot subscription, or laptop development-tool installation is part of the primary route.

## 0.2 Create your own repository from the original template

1. Open [github-samples/pets-workshop](https://github.com/github-samples/pets-workshop).
2. Select **Use this template > Create a new repository**. Do not open a codespace on the upstream template.
3. Choose your username as **Owner**, name the repository `pets-devsecops`, select **Public**, and leave **Include all branches** off. Use an approved organization only if you will have admin access and its policies allow the lab.
4. Select **Create repository from template**. If that name already exists, choose a new name and use it consistently.
5. Confirm the URL belongs to your account, the default branch is `main`, and **Settings** and **Actions** are accessible. The application includes `app/server/app.py` and `app/client/package-lock.json`.

The original Pets repository is the only application template. The companion provides additions, not a replacement application or history to merge. This kit targets source revision `d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a`. If the live template has drifted incompatibly, the organizer must update and retest the companion; do not overwrite the application with an old snapshot.

## 0.3 Open the learner codespace

1. On **your learner repository**, select `main`, then **Code > Codespaces**.
2. Read the message showing who will pay. Use the smallest suitable permitted machine, normally two cores, and the default image. If you need to inspect machine options, use the Codespaces menu's **New with options**, keeping this learner repository and `main` selected.
3. Select **Create codespace on main** (or **Create codespace** on the options page). If you already have a codespace for this learner copy, reopen it instead of creating another.
4. Wait for browser-based VS Code and repository initialization to finish. Select **Terminal > New Terminal**.
5. Inspect the checkout that Codespaces already cloned:

   ```bash
   repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root"
   pwd
   git remote get-url origin
   git branch --show-current
   git status --short
   ```

The root should be under `/workspaces`, `origin` should name your learner repository, the branch should be `main`, and there should be no unrelated changes. Do not assume a fixed folder name or clone the app again. A wrong origin or a prompt to fork means you should stop and return to your own learner repository.

Git and Bash are provided by the default environment. Do not add a required `.devcontainer`, rebuild the image, install app dependencies, or start the app. Builds, tests, and scans run in Actions. Keep any forwarded ports private; this lab adds no app hosting.

## 0.4 Fetch the companion beside the existing checkout

Use one version throughout: **v0.1.2**, with its [release/checksum](https://github.com/frye/pets-devsecops-workshop/releases/tag/v0.1.2) and [manifest](workshop-kit.json).

1. From the learner root in the Codespaces terminal, fetch the public tag without adding a remote:

   ```bash
   git fetch --no-tags https://github.com/frye/pets-devsecops-workshop.git refs/tags/v0.1.2 &&
   KIT_COMMIT=$(git rev-parse 'FETCH_HEAD^{commit}') &&
   printf '%s\n' "$KIT_COMMIT"
   ```

2. Compare the printed commit with the commit recorded on that release. Stop if it differs. Keep this terminal open: the next command uses the verified `KIT_COMMIT`, not a later `FETCH_HEAD` that VS Code background fetching could replace. If the variable is lost, fetch and capture it again, then compare it with the release. Do not disable global auto-fetch, merge the companion, or request broader credentials to read this public kit.
3. Extract the companion root into a versioned sibling directory. Both paths below must be new:

   ```bash
   test ! -e ../pets-devsecops-kit-v0.1.2 &&
   test ! -e ../pets-devsecops-kit-v0.1.2.tar &&
   mkdir ../pets-devsecops-kit-v0.1.2 &&
   git archive --format=tar --output=../pets-devsecops-kit-v0.1.2.tar "$KIT_COMMIT" &&
   tar -xf ../pets-devsecops-kit-v0.1.2.tar -C ../pets-devsecops-kit-v0.1.2
   ```

4. In **File > Open File**, open `../pets-devsecops-kit-v0.1.2/README.md` and `../pets-devsecops-kit-v0.1.2/scripts/prepare-devsecops.sh` relative to your learner root, or use their full paths shown under `/workspaces`.

Keep the kit outside the application checkout but inside `/workspaces`. Saved files there persist across stop/start and container rebuilds; they do not survive deleting the codespace. Do not extract into `/tmp`, overwrite an existing kit blindly, commit the kit into your app, or pipe a remote script into a shell.

## 0.5 Install, review, commit, and push two workflows

Run the inspected helper from the learner root:

```bash
bash "../pets-devsecops-kit-v0.1.2/scripts/prepare-devsecops.sh" --repo . --check
bash "../pets-devsecops-kit-v0.1.2/scripts/prepare-devsecops.sh" --repo . --apply
```

The first command is read-only. Apply verifies origin, branch, application fingerprints, and local changes before copying only:

```text
.github/workflows/ci.yml
.github/workflows/dependency-review.yml
```

Identical content is a no-op. The helper never changes credentials, identity, remotes, GitHub settings, or history; it does not commit, push, or install software. Resolve a refusal using [troubleshooting](take-home/troubleshooting.md), without discarding work.

Codespaces already configures repository authentication. Keep it; never print or replace its developer token or paste a PAT. That credential is separate from an Actions job token. Check your commit author privately:

```bash
git config --get user.name
git config --get user.email
```

If missing or unsuitable for a public commit, use the [repository-local identity recovery](take-home/troubleshooting.md#commit-identity). Do not change global credentials or settings.

Review and stage exactly the two starter files:

```bash
git status --short
git add -- .github/workflows/ci.yml .github/workflows/dependency-review.yml
git diff --cached -- .github/workflows/ci.yml .github/workflows/dependency-review.yml
```

If only those expected files are staged:

```bash
git commit -m "Configure DevSecOps workshop CI"
git push origin main
```

Skip an empty commit if identical files are already committed, but verify they are on remote `main`. A save or local commit alone is not a push. If workflow-file authentication fails, preserve the files and follow the specific [Codespaces recovery](take-home/troubleshooting.md#codespaces-access-and-recovery); do not widen token permissions or install a bootstrap workflow.

Only `ci.yml` and `dependency-review.yml` belong in prework. Do not install `release-simulation.yml`, `token-permissions.yml`, solutions, or fixtures yet.

## 0.6 Verify Actions on GitHub

1. Open your learner repository's **Actions** tab on GitHub.com. Enable workflows if prompted and policy permits.
2. Open the **CI** run on `main`. Confirm `api-tests` and `client-build` succeed.
3. If no run appeared, confirm the two files are on remote `main`, then use **Actions > CI > Run workflow > main**. This runs the same checks.
4. Save the passing run URL. Diagnose failure, cancellation, or skipped jobs before continuing.

Python 3.14, Node 24, dependency installation, and builds run on the Actions runner, not in the codespace. Dependency review is PR-triggered and is checked in 0.8.

## 0.7 Configure security on GitHub

1. Open **Settings > Advanced Security** and confirm **Dependency graph** is enabled. Account UI labels can vary; use the linked documentation if a control is grouped differently.
2. Under **CodeQL analysis**, select **Set up > Default**, confirm Python is detected, review other detected languages, and select **Enable CodeQL**. Do not add advanced setup alongside default setup.
3. Confirm **Secret scanning** and repository **Push protection** are enabled. An account-level protection setting is not a substitute. Do not test a fixture or any credential during setup.
4. Wait for successful initial analysis. In **Security and quality > Code scanning**, find **Flask app is run in debug mode**, rule `py/flask-debug`, at `app/server/app.py`.
5. Record the analysis and alert links; leave this finding open for lesson 3.

The default Python suite's high-severity debug finding was observed in the earlier rehearsal. If it is absent, pending, or analysis failed in your copy, report the run URL, source state, and kit version. Do not add an unsafe endpoint to manufacture a finding.

## 0.8 Create your working branch and PR

Both workflows must be on remote `main` before this branch exists.

1. Return to the same codespace. Confirm a clean prepared `main`:

   ```bash
   git status --short
   git branch --show-current
   git switch -c exercise/shelter-change
   ```

2. In the Codespaces editor, create and save `workshop-notes.md` in the learner root:

   ```markdown
   # Workshop notes

   Goal: improve the shelter's delivery process.
   ```

3. Commit and push only that file:

   ```bash
   git add -- workshop-notes.md
   git commit -m "Start the shelter workshop"
   git push -u origin exercise/shelter-change
   ```

4. On GitHub.com, open the PR with **base: main**, **compare: exercise/shelter-change**, and title **Prepare the shelter for a safer release**. Both branches must belong to your learner repository.
5. Confirm `api-tests`, `client-build`, and `dependency-review` pass on the harmless change and CodeQL analysis operates. The outstanding default-branch debug finding is intentional.
6. Leave the PR open and unmerged. If it already exists, resume it rather than opening a duplicate.

## 0.9 Checkpoint: ready for Step 1

| Check | Your evidence |
|---|---|
| Account and public learner copy | Repository URL, accessible settings, permitted usage/payer |
| Codespaces primary route | Existing checkout verified, terminal opens, companion fetch and workflow push succeeded |
| Kit | v0.1.2 sibling under `/workspaces`; two matching workflows on remote `main` |
| Functional baseline | Successful API/build run URL |
| Security baseline | Successful analysis, expected debug finding, dependency graph and secret protection enabled |
| Working PR | Open own-repo starter PR with three passing core checks |

Send repository, PR, baseline-run URLs, and kit version through the event's existing readiness channel. Confirm Codespaces startup/fetch/push worked, or explicitly name the fallback used. Do not share credentials, token values, private connection details, or a claim that a fallback proves Codespaces worked.

## 0.10 Stop and reuse the same codespace

Use one codespace for this learner repository throughout the workshop and take-home labs. Saving files preserves them in the workspace; committing records them locally; pushing makes the intended commits available on GitHub.

Before leaving, save edits, commit and push safe intended work, and check the remote branch. Never push the rejected secret-training commit as a backup. Select **Codespaces: Stop Codespace** from the VS Code Command Palette, or **Stop codespace** in the menu for this space at [github.com/codespaces](https://github.com/codespaces). Confirm it stopped; merely closing the browser tab does not stop compute.

Stopped spaces still consume storage. Reopen the same named space to resume. Delete it only after preserving all needed work and evidence; deletion removes the workspace and sibling kit. If quota prevents resuming, see [exporting changes](https://docs.github.com/en/codespaces/troubleshooting/exporting-changes-to-a-branch) and review what will be published before exporting.

## Fallback A: local VS Code and Git

Use this only when Codespaces access, quota, policy, or connectivity is unsuitable. You need an existing editor, Bash-compatible terminal (macOS/Linux or Windows Git Bash), and Git authentication. No local app runtime is required.

Clone **your learner repository** into a new local folder, substituting your username:

```bash
git clone https://github.com/YOUR-OWNER/pets-devsecops.git
cd pets-devsecops
```

Continue with 0.4's pinned fetch, sibling extraction, and 0.5's helper/commit steps. The sibling is outside this local clone rather than under `/workspaces`; the Codespaces-specific lifecycle does not apply. Use your existing authentication or VS Code browser sign-in, not a pasted PAT or global work-identity change. Later terminal exercises use the same commands.

## Fallback B: GitHub file editor

Use this when neither Codespaces nor existing local Git is available.

1. On your learner repository's `main`, open the [raw CI starter](https://raw.githubusercontent.com/frye/pets-devsecops-workshop/v0.1.2/starter/ci.yml), then **Add file > Create new file**. Name it `.github/workflows/ci.yml` and paste the entire raw file, without Markdown fences.
2. Commit directly to `main` for initial setup. Repeat with [raw dependency review](https://raw.githubusercontent.com/frye/pets-devsecops-workshop/v0.1.2/starter/dependency-review.yml) at `.github/workflows/dependency-review.yml`.
3. Compare both committed files with this kit; do not overwrite different existing workflows blindly. Complete 0.6 and 0.7 on GitHub.
4. For 0.8, create the same `workshop-notes.md` on `main`, choose **Create a new branch for this commit and start a pull request**, and name it `exercise/shelter-change`. Complete the same PR/checkpoint checks.
5. For later edits, select the intended branch first and use the same version's supplied content. Commit only the lesson's changes, then inspect checks on GitHub.

The file editor cannot execute terminal commands. Its secret exercise blocks a web commit and repairs an uncommitted edit; it does not demonstrate terminal history repair. Use lesson 5's separately labeled fallback. `github.dev` is an editor, not a Codespaces terminal.

## Resources

[Create a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [source control](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace), [persistent workspace](https://docs.github.com/en/codespaces/about-codespaces/deep-dive), [usage and billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), [authentication](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-authentication-to-a-repository), and [stop/resume](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace).

[Account signup](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github), [template copies](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning), [web editing](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files), and [supported secret patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns).

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|
