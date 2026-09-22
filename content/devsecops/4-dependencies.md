# 4. Review a vulnerable dependency change

| [Previous: code scanning](3-code-scanning.md) | [Next: secrets](5-secrets.md) |
|:---|---:|

Budget: 15 minutes. A volunteer proposes a package change. Your review should catch a known vulnerability before it reaches `main`.

## Why it matters

Dependency review evaluates the packages a PR introduces. Dependabot alerts monitor dependencies already present; version-update PRs keep them current. None of these replaces testing an update.

> [!WARNING]
> This exercise uses an unused manifest. Never install its packages or merge its PR. The files in this kit are inert `.txt` handouts; only your isolated exercise branch gets a real `requirements.txt`.

## Try it

1. Return briefly to your code-fix PR and record its current results. Then inspect `.github/dependabot.yml`: it covers npm in `/app/client`. Pip and Actions configuration belongs to the take-home lab; do not edit it now.
2. In the Codespaces terminal, confirm your previous work is committed and the tree is clean, then create the isolated branch from prepared `main`:

   ```bash
   git status --short
   git switch main
   git switch -c exercise/dependency-review
   ```

   If that branch already exists, inspect it and resume the work instead of overwriting it.
3. Copy the fetched kit's inert before fixture into the unused lab directory:

   ```bash
   test ! -e workshop-lab/dependency/requirements.txt &&
   mkdir -p workshop-lab/dependency &&
   cp ../pets-devsecops-kit-v0.1.2/fixtures/dependency-before.txt workshop-lab/dependency/requirements.txt
   ```

   Open **`workshop-lab/dependency/requirements.txt`** in the Codespaces editor and confirm it contains exactly:

   ```text
   PyJWT==2.3.0
   ```

4. Review, commit, and push only this manifest:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Add isolated dependency review training fixture"
   git push -u origin exercise/dependency-review
   ```

   On GitHub.com, open a PR against your own `main` titled **Training only: dependency review; do not merge**. The workflow on `main` already reports `dependency-review`. Neither CI job reads this lab directory.
5. Wait for the initial dependency review result. Inspect the PR's dependency diff and confirm it lists PyJWT, the manifest path, and version 2.3.0. Open the failed `dependency-review` job and record the high-severity advisory and run URL.
6. Only after observing the failure, use the Codespaces editor to replace the file's one line with the content of `../pets-devsecops-kit-v0.1.2/fixtures/dependency-after.txt`:

   ```text
   PyJWT==2.14.0
   ```

7. Save the file, commit the repair on the same branch, and inspect its Actions result on GitHub:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Repair the isolated dependency fixture"
   git push
   ```

   Record the passing `dependency-review` run for this revision. Leave the PR unmerged for take-home, or close it without merging. Never install the fixture in Codespaces, on a laptop, or in CI.

If needed, the [local Git fallback](0-setup.md#fallback-a-local-vs-code-and-git) uses these same commands. In the [file-editor fallback](0-setup.md#fallback-b-github-file-editor), create the same manifest from `main` on a new `exercise/dependency-review` branch, observe failure, then edit its one line and commit the repair on that branch.

## Read the advisory

[GHSA-ffqj-6fqr-9h24](https://github.com/advisories/GHSA-ffqj-6fqr-9h24) is high severity and affects PyJWT `>=1.5.0,<2.4.0`. Version 2.3.0 is in that range. The first patch for that advisory was 2.4.0, but it is not the current repair used here: [GHSA-752w-5fwx-jx9f](https://github.com/advisories/GHSA-752w-5fwx-jx9f) affects versions through 2.11.0.

The supplied repair is 2.14.0. The GitHub Advisory API returned no matching advisories for that version during authoring; this is a dated lookup, not a promise that it will remain vulnerability-free. A new advisory may require a new kit version. [Technical sources](sources.md) record the check.

The starter fails on **high** or **critical** severity across runtime, development, and unknown scopes. A green job with an empty dependency diff is not proof of fixture detection. If the manifest is absent, stop and report discovery failure; do not lower the threshold or install the fixture to force a result.

## Checkpoint

Your evidence has a failed run, the observed advisory/version, the one-line repair, and a passing run. If the first result is still pending at minute 53, move to secrets and return during the demonstrations. Do not repair before seeing the initial failure and then claim a red-to-green cycle.

## Resources

[Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) and [Dependabot quickstart](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart) explain the separate controls. [Supported dependency ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems) describes manifest support.

| [Previous: code scanning](3-code-scanning.md) | [Next: secrets](5-secrets.md) |
|:---|---:|
