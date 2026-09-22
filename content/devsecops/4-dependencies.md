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
2. Create `exercise/dependency-review` from prepared `main`, not from the working PR. In the web editor, start on `main`, create the file below, and choose a new branch when committing. Terminal users run `git switch main` and `git switch -c exercise/dependency-review` from a clean checkout of the prepared baseline.
3. Create **`workshop-lab/dependency/requirements.txt`** with exactly:

   ```text
   PyJWT==2.3.0
   ```

4. Commit, push if using Git, and open a PR against your own `main` titled **Training only: dependency review; do not merge**. The workflow on `main` already reports `dependency-review`. Neither CI job reads this lab directory.
5. Wait for the initial dependency review result. Inspect the PR's dependency diff and confirm it lists PyJWT, the manifest path, and version 2.3.0. Open the failed `dependency-review` job and record the high-severity advisory and run URL.
6. Only after observing the failure, replace the file's one line with:

   ```text
   PyJWT==2.14.0
   ```

7. Commit the repair on the same branch and inspect the new result. Record the passing `dependency-review` run for the repaired commit. Leave this PR unmerged for take-home, or close it without merging.

For terminal edits, stage only `workshop-lab/dependency/requirements.txt`, commit, and use `git push -u origin exercise/dependency-review` for the first push; subsequent pushes can use `git push`.

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
