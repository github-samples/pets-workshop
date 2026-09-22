# 3. Maintain the dependency baseline

| [Previous: approve a release](2-approve-a-release.md) | [Next: optional workload identity](4-workload-identity.md) |
|:---|---:|

## Why it matters

New advisories can affect a previously reviewed revision. Update configuration helps surface changes, but someone still owns review, testing, and rollout.

## 1. Extend Dependabot coverage

1. [Resume your existing codespace](0-resume.md). From a clean learner root, update your own `main` and branch:

   ```bash
   git status --short
   git fetch origin
   git switch main
   git merge --ff-only origin/main
   git switch -c exercise/dependency-maintenance
   ```

2. Open the fetched kit's [configuration](../solutions/dependabot.yml) in the editor, then copy it to the learner copy:

   ```bash
   cp ../pets-devsecops-kit-v0.1.2/solutions/dependabot.yml .github/dependabot.yml
   ```

   Review this intentional configuration replacement. It preserves the npm groups and adds these entries under `updates`:

   ```yaml
     - package-ecosystem: pip
       directory: /app/server
       schedule:
         interval: weekly
     - package-ecosystem: github-actions
       directory: /
       schedule:
         interval: weekly
   ```

3. In the Codespaces editor, pin the application's three direct requirements in `app/server/requirements.txt` to the tested baseline and save:

   ```text
   Flask==3.1.3
   SQLAlchemy==2.0.54
   Flask-SQLAlchemy==3.1.1
   ```

4. Commit and push only the two intended files:

   ```bash
   git add -- .github/dependabot.yml app/server/requirements.txt
   git diff --cached
   git commit -m "Maintain Python and Actions dependencies"
   git push -u origin exercise/dependency-maintenance
   ```

   On GitHub.com, open the PR and inspect core checks and policy results. Merge only after they pass. Do not include `workshop-lab/dependency/requirements.txt`, or install these requirements in the codespace during the lab.

The complete config avoids reconstructing indentation from the excerpt. If needed, [local Git](../0-setup.md#fallback-a-local-vs-code-and-git) uses these commands; the [file-editor fallback](../0-setup.md#fallback-b-github-file-editor) edits the same two files on the new branch and opens its PR.

## 2. Understand the Python snapshot

The upstream manifest starts unpinned. To keep participant prework at two files, both supplied functional workflows contain the same exact-version constraints in the **Install workshop Python baseline** step. They install only the application's manifest, never the lab fixture.

The constraints cover the resolved dependencies for the selected runtimes, including Linux's `greenlet`. They pin versions without locking package hashes. Package indexes and advisories can change, so these versions still need ongoing review.

A future pip update may conflict with the constraints. That failure is intentional: review the new resolved versions, update the constraints in **both** `ci.yml` and `release-simulation.yml` if installed, then rerun tests and review advisories. Do not delete the constraint flag just to obtain green checks.

### Maintainer-only snapshot regeneration

The commands below are for future kit maintenance in a separately approved disposable environment, outside this learner exercise. Do not run them in the participant codespace or require a laptop Python installation:

```bash
python3 -m venv /path/to/disposable-resolution-env
/path/to/disposable-resolution-env/bin/python -m pip install -r app/server/requirements.txt
/path/to/disposable-resolution-env/bin/python -m pip check
/path/to/disposable-resolution-env/bin/python -m pip freeze
```

Replace the path with a new, unused directory. On Windows, use that environment's `Scripts/python.exe`. Review the resulting versions and platform markers; a macOS resolution alone does not prove Ubuntu compatibility. Copy only the reviewed constraints into the two workflow steps, and use the standard Ubuntu Actions runs to validate them.

## 3. Verify configuration and review future updates

1. On remote `main`, confirm the file parses as version 2 and has exactly npm `/app/client`, pip `/app/server`, and `github-actions` `/` entries.
2. Open **Insights > Dependency graph > Dependabot** where available and inspect update-job/configuration errors. Confirm the configured directories exist.
3. In **Settings > Advanced Security**, review dependency graph, Dependabot alerts, and Dependabot security updates. Enable available controls only within your repository and policy.
4. A weekly version-update schedule does not promise an immediate PR. Security updates depend on an applicable advisory and a supported fix. Record configuration acceptance independently of PR arrival.
5. When a bot PR arrives, inspect the advisory/release notes, package and lockfile changes, exact action SHA if relevant, permissions, and tests. Require the same policy before merging. Do not auto-merge an update merely because a bot opened it.

## Checkpoint

Save the merged configuration PR and evidence of accepted update configuration. Record any update PR as a later observation, not a guaranteed workshop result. Assign an owner to review future alerts.

Save and push safe work, then explicitly stop the codespace when pausing. Keep the kit for the next lab and preserve needed work before deleting a space.

## Resources

[Dependabot configuration options](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference), [security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates), and [pip repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/).

| [Previous: approve a release](2-approve-a-release.md) | [Next: optional workload identity](4-workload-identity.md) |
|:---|---:|
