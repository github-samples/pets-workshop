# 0. Prepare your shelter repository

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|

## Why it matters

Preparing the repository before the event gives you time to resolve account policies and Actions failures. The first eight minutes of the event are a readiness check, not an account-creation or installation session.

> [!IMPORTANT]
> Use the [v0.1.0 companion kit](https://github.com/frye/pets-devsecops-workshop/tree/v0.1.0) and read its [readiness gates](readiness.md). This prerelease has automated and terminal authoring evidence. A fresh browser-only learner walkthrough and measured timing are still outstanding. The readiness register links the observed CodeQL baseline.

## 0.1 Choose an account

1. Sign in at [GitHub.com](https://github.com). Reuse an existing account if it can own a public repository and administer Actions and security settings.
2. Check your employer's policy before using a work account, managed laptop, or personal account for public training. Do not work around restrictions. An approved paired/demo arrangement is possible, but it does not satisfy every individual checkpoint.
3. Enterprise Managed Users cannot create public repositories. If policy permits, use a separate personal account. A GitHub Enterprise Server or GHE.com identity is not automatically a GitHub.com account.
4. If you need a personal account, use [GitHub signup](https://github.com/signup), select the free option, and verify an email you control. Do not use an email already verified for an Enterprise Managed User. Configure two-factor authentication and save recovery information securely.
5. Check the username in the profile menu. This account will own the learner repository and your commits. Do not share passwords or tokens with helpers.

## 0.2 Create your public learner repository

1. Open [github-samples/pets-workshop](https://github.com/github-samples/pets-workshop).
2. Select **Use this template > Create a new repository**. This is a template copy, not a fork.
3. Choose your username as **Owner**, name the repository `pets-devsecops`, select **Public**, and leave **Include all branches** off. If the name is taken, choose another and use it consistently.
4. Select **Create repository from template**. Confirm the URL names your account, not `github-samples`. Both **Settings** and **Actions** must be accessible.
5. Confirm the default branch is `main` and the repository contains `app/server/app.py` and `app/client/package-lock.json`.

The template flow copies the current upstream contents. This kit was prepared against `d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a`; incompatible drift requires an updated, retested companion kit. The original Pets repository is the only learner application template. Do not replace your application with an old snapshot.

## 0.3 Obtain one kit version

The companion supplies every customization and guide. Use one version throughout: **v0.1.0**, with [manifest](workshop-kit.json) and [release/checksum](https://github.com/frye/pets-devsecops-workshop/releases/tag/v0.1.0).

For the browser route, open the [version-pinned guide](https://github.com/frye/pets-devsecops-workshop/blob/v0.1.0/0-setup.md) and these raw files:

- [Raw CI starter](https://raw.githubusercontent.com/frye/pets-devsecops-workshop/v0.1.0/starter/ci.yml)
- [Raw dependency-review starter](https://raw.githubusercontent.com/frye/pets-devsecops-workshop/v0.1.0/starter/dependency-review.yml)

For the terminal route, create your repository from the original template first. Replace `YOUR-OWNER` below, clone that learner repository, and fetch the companion tag without adding a remote:

```bash
git clone https://github.com/YOUR-OWNER/pets-devsecops.git
cd pets-devsecops
git fetch --no-tags https://github.com/frye/pets-devsecops-workshop.git refs/tags/v0.1.0
git rev-parse 'FETCH_HEAD^{commit}'
```

Compare the printed commit with the commit recorded on the versioned release. Stop if it differs. The fetch does not change your branch, index, origin, or working files; template histories do not need a common ancestor.

Extract the companion root to a new sibling directory. These output paths must not already exist. The chained commands stop on failure and do not pipe an archive into an unchecked extractor:

```bash
test ! -e ../pets-devsecops-kit-v0.1.0 &&
test ! -e ../pets-devsecops-kit-v0.1.0.tar &&
mkdir ../pets-devsecops-kit-v0.1.0 &&
git archive --format=tar --output=../pets-devsecops-kit-v0.1.0.tar FETCH_HEAD &&
tar -xf ../pets-devsecops-kit-v0.1.0.tar -C ../pets-devsecops-kit-v0.1.0
```

Open the extracted README and script before running anything. Keep the whole kit, including take-home files, outside the learner clone. If you prefer downloading the release ZIP, extract it outside the clone and substitute that script path below. Never pipe a remote script into a shell.

Only these two files belong in live prework:

| Source in this kit | Destination in your learner repository |
|---|---|
| [starter/ci.yml](starter/ci.yml) | `.github/workflows/ci.yml` |
| [starter/dependency-review.yml](starter/dependency-review.yml) | `.github/workflows/dependency-review.yml` |

Do not install `release-simulation.yml`, the solutions, or any fixture yet. Do not add a companion remote or use `git pull` to combine unrelated histories.

## 0.4 Install the core workflows

### Web route (narrated)

1. In your learner repository, select `main`.
2. Open [starter/ci.yml](starter/ci.yml) from this exact kit and copy the complete file.
3. Select **Add file > Create new file** in your learner repository. Enter `.github/workflows/ci.yml` as the filename and paste the YAML.
4. Select **Commit changes**, use the message `Configure workshop CI`, and commit directly to `main`. This direct commit is initial setup, before merge rules are enabled.
5. Repeat for [starter/dependency-review.yml](starter/dependency-review.yml), using destination `.github/workflows/dependency-review.yml` and message `Configure dependency review`.
6. Compare the two committed files with the starters. If either destination already exists and differs, stop and use [conflicting workflows](take-home/troubleshooting.md); do not overwrite it blindly.

### Terminal route

Use macOS/Linux Bash or Git Bash on Windows. Git and authentication must already work. VS Code's browser sign-in flow is an option; do not paste a PAT into a command or file, or change corporate Git identity settings globally.

Git's commit author identity is separate from GitHub authentication. From your learner clone, inspect the name and email that Git would use:

```bash
git config --get user.name
git config --get user.email
```

If either is missing, or the inherited work email is unsuitable for a public training commit, copy your account's exact noreply address from **GitHub Settings > Emails**. Replace both quoted values below before running these repository-local commands:

```bash
git config --local user.name "YOUR DISPLAY NAME"
git config --local user.email "YOUR EXACT GITHUB NOREPLY ADDRESS"
```

These commands affect only this clone; the helper never sets identity. Do not share the printed email with helpers or change global corporate settings. The web route uses your GitHub account's commit settings and needs no local Git configuration.

1. From the learner clone created in 0.3, check your state:

   ```bash
   git status --short
   git branch --show-current
   ```

2. Confirm `main` and no unrelated changes. Read [the helper](scripts/prepare-devsecops.sh) before running it:

   ```bash
   bash "../pets-devsecops-kit-v0.1.0/scripts/prepare-devsecops.sh" --repo . --check
   bash "../pets-devsecops-kit-v0.1.0/scripts/prepare-devsecops.sh" --repo . --apply
   ```

3. The first command is read-only. The second copies only the two workflow files after checking origin, branch, application fingerprints, and local changes. It never commits, pushes, installs software, changes remotes, authenticates, or changes GitHub settings. Its output names each copied or unchanged file.
4. Review and stage only those files:

   ```bash
   git status --short
   git add -- .github/workflows/ci.yml .github/workflows/dependency-review.yml
   git diff --cached -- .github/workflows/ci.yml .github/workflows/dependency-review.yml
   ```

5. If the staged diff contains only the two expected starters:

   ```bash
   git commit -m "Configure DevSecOps workshop CI"
   git push origin main
   ```

Identical reruns do nothing. If the files were already committed, skip the empty commit; verify they are on remote `main`. A helper refusal leaves your files in place. Follow its error and the troubleshooting guide instead of resetting, stashing, or disabling its checks.

## 0.5 Verify Actions

1. Open **Actions**. Enable workflows if GitHub asks and your policy allows it.
2. Open the **CI** run on `main`. Confirm the exact jobs `api-tests` and `client-build` succeed.
3. If no run appeared, verify both files exist on remote `main`. Select **Actions > CI > Run workflow**, choose `main`, and run it. The manual route runs the same tests and build.
4. Save the successful run URL. A failure, cancellation, or skipped job is not a passing baseline. Diagnose it before continuing.

The API uses Python 3.14 and a version-constrained dependency snapshot on the runner. The client uses Node 24 and `npm ci`; Astro 6 requires at least Node 22.12. Neither runtime is needed on your laptop. Dependency review reports on PRs, so it is checked in 0.7.

## 0.6 Configure security

1. Open **Settings > Advanced Security**. GitHub may group these controls under **Code security** in some accounts; use the linked product documentation if the label differs. Confirm the **Dependency graph** is enabled.
2. Under **CodeQL analysis**, select **Set up > Default**. Confirm Python is detected, review any additional detected languages, and select **Enable CodeQL**. Do not also install an advanced CodeQL workflow.
3. Confirm **Secret scanning** and repository **Push protection** are enabled. An account-level push-protection setting does not replace this repository check. Do not test any token during prework.
4. Wait for the initial CodeQL analysis to finish. Open **Security and quality > Code scanning** and locate **Flask app is run in debug mode**, rule `py/flask-debug`, at `app/server/app.py`.
5. Record the analysis and alert links. Leave this finding open for lesson 3.

The rule is documented in the default Python suite with security severity 7.5 and was observed in the authorized rehearsal copy. If your analysis fails, stays pending, or produces no expected finding, record the state and contact the organizer with the run URL and kit version. Do not add an unsafe endpoint or pretend the baseline is ready.

## 0.7 Open your working PR

Both workflows must be on remote `main` before creating this branch.

1. On `main`, select **Add file > Create new file**. Name it `workshop-notes.md` and add:

   ```markdown
   # Workshop notes

   Goal: improve the shelter's delivery process.
   ```

2. Select **Commit changes**, choose **Create a new branch for this commit and start a pull request**, and name it `exercise/shelter-change`.
3. Open the PR with **base: main**, **compare: exercise/shelter-change**, title **Prepare the shelter for a safer release**. Both branches must belong to your learner repository.
4. Confirm `api-tests`, `client-build`, and `dependency-review` all pass. Confirm CodeQL analysis is operating; the outstanding baseline debug finding is intentional.
5. Leave this PR open and unmerged.

For terminal users, start on clean prepared `main`, run `git switch -c exercise/shelter-change`, create the same file in your editor, then run:

```bash
git add -- workshop-notes.md
git commit -m "Start the shelter workshop"
git push -u origin exercise/shelter-change
```

Open the PR in GitHub as described above. If a working PR already exists, inspect it and resume it rather than creating a duplicate.

## Checkpoint: ready for Step 1

| Check | Your evidence |
|---|---|
| Eligible account and owned public learner copy | Repository URL and accessible settings |
| Correct kit | Version and two matching workflows on remote `main` |
| Functional baseline | Successful `api-tests` and `client-build` run URL |
| Security baseline | Successful analysis, expected debug alert, dependency graph and secret protection enabled |
| Working PR | Open `exercise/shelter-change` PR, three core checks passing |
| Editing works | Your harmless web commit or Git push succeeded |

Send the repository URL, working-PR URL, baseline-run URL, and kit version through the event's existing readiness channel. Do not send credentials or private screenshots. Keep the PR, Actions, and security tabs open.

The [troubleshooting guide](take-home/troubleshooting.md) covers account restrictions, drift, conflicts, authentication, missing checks, failed analysis, and unavailable settings. Incomplete rows need advance help; the opening eight minutes cannot absorb setup for a full room.

## Resources

[Create an account](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github), [template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [VS Code and GitHub](https://code.visualstudio.com/docs/sourcecontrol/github), [web editing](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files), [CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning), and [supported secret patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns).

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|
