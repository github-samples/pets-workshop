# 3. Maintain the dependency baseline

| [Previous: approve a release](2-approve-a-release.md) | [Next: troubleshooting](troubleshooting.md) |
|:---|---:|

## Why it matters

New advisories can affect a previously reviewed revision. Update configuration helps surface changes, but someone still owns review, testing, and rollout.

## 1. Extend Dependabot coverage

1. Create `exercise/dependency-maintenance` from current `main`.
2. Replace `.github/dependabot.yml` with [the supplied configuration](../solutions/dependabot.yml). It preserves the npm groups and adds these entries under `updates`:

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

3. Pin the application's three direct Python requirements in `app/server/requirements.txt` to the kit's tested baseline:

   ```text
   Flask==3.1.3
   SQLAlchemy==2.0.54
   Flask-SQLAlchemy==3.1.1
   ```

4. Open a PR, review the diff, and wait for core checks and policy results. Merge only after they pass. Do not include `workshop-lab/dependency/requirements.txt`.

The complete [configuration](../solutions/dependabot.yml) is available so you do not have to reconstruct YAML indentation from the excerpt. Terminal users stage only `.github/dependabot.yml` and `app/server/requirements.txt`, commit, push the branch, and open the PR in GitHub.

## 2. Understand the Python snapshot

The upstream manifest starts unpinned. To keep participant prework at two files, both supplied functional workflows contain the same exact-version constraints in the **Install workshop Python baseline** step. They install only the application's manifest, never the lab fixture.

The constraints cover the resolved dependencies for the selected runtimes, including Linux's `greenlet`. They pin versions without locking package hashes. Package indexes and advisories can change, so these versions still need ongoing review.

A future pip update may conflict with the constraints. That failure is intentional: review the new resolved versions, update the constraints in **both** `ci.yml` and `release-simulation.yml` if installed, then rerun tests and review advisories. Do not delete the constraint flag just to obtain green checks.

For maintainers who already have Python, use a disposable environment to resolve an update; this is not an attendee prerequisite:

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

## Resources

[Dependabot configuration options](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference), [security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates), and [pip repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/).

| [Previous: approve a release](2-approve-a-release.md) | [Next: troubleshooting](troubleshooting.md) |
|:---|---:|
