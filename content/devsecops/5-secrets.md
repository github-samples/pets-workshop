# 5. Block a secret before it enters history

| [Previous: dependencies](4-dependencies.md) | [Next: merge policy](6-merge-policy.md) |
|:---|---:|

Budget: 12 minutes. A volunteer pastes a credential while troubleshooting. Each participant's intended outcome is a real protection block and a clean retry.

## Why it matters

A later deletion commit leaves the earlier value in Git history. Push protection can stop supported values before they arrive; a real exposure still requires revocation or rotation and investigation.

> [!WARNING]
> Use only [the supplied delimiter-masked fixture](fixtures/secret-training.txt), which the official GitHub Skills source identifies as inactive. The earlier local-terminal block/repair was observed; an actual Codespaces attempt and the file-editor fallback still need their own rehearsal. Read [the provenance and route status](fixtures/secret-validation.md). Never use an active credential, including the developer token configured inside Codespaces, or invent a value to force detection.

## Before the attempt

1. Confirm repository **Secret scanning** and **Push protection** are enabled.
2. Read the fixture record's inactive-source evidence, kit version, supported pattern, route results, and date. The organizer must finish the supported-route rehearsal before presenting this as a verified event exercise.
3. Work on `exercise/secret-protection`, created from prepared `main`, separate from your code and dependency PRs. Do not pre-seed the fixture into the template or any published branch.

## Primary route: Codespaces terminal

1. In the same Codespaces terminal, confirm the previous exercise is saved, committed, and the working tree is clean. Create the isolated branch:

   ```bash
   git status --short
   git switch main
   git switch -c exercise/secret-protection
   ```

2. Open `../pets-devsecops-kit-v0.1.2/fixtures/secret-training.txt` in the Codespaces editor. Copy its one line into a new `secret-training.txt` in the learner root, remove the literal `<REMOVE_ME>` delimiter in that new file, and save. Leave the kit copy unchanged. Never print a token or dump the Codespaces environment. Then run:

   ```bash
   git add -- secret-training.txt
   git commit -m "Attempt approved nonfunctional training fixture"
   git push -u origin exercise/secret-protection
   ```

3. Confirm GitHub rejects the push for secret protection, not authentication or a network error. Keep the commit/path evidence with the fixture value and bypass URL redacted. Do not follow a bypass link.
4. For this single, newest, unpublished training commit, replace the file in the Codespaces editor with `TRAINING_VALUE_REMOVED` and save. Rewrite that unpublished commit, then push normally:

   ```bash
   git add -- secret-training.txt
   git diff --cached
   git commit --amend --no-edit
   git push -u origin exercise/secret-protection
   ```

5. Confirm the clean push succeeds and the placeholder is visible on your remote branch. Do not use force push. Leave the branch unmerged.

The narrow amend above is an explicit part of this exercise. If the rejection lists several affected unpublished commits, editing only the latest one is insufficient. Stop the timed path and follow [the multi-commit recovery](take-home/troubleshooting.md#more-than-one-unpublished-secret-commit), checking every affected commit. Never rewrite someone else's published work.

## Fallbacks

The [local VS Code/Git fallback](0-setup.md#fallback-a-local-vs-code-and-git) uses the same isolated branch, blocked push, and unpublished-commit repair. Record that you used local Git, not Codespaces.

For the [GitHub file-editor fallback](0-setup.md#fallback-b-github-file-editor):

1. On your learner repository, create `exercise/secret-protection` from `main`.
2. Select **Add file > Create new file**, name it `secret-training.txt`, paste the same supplied fixture, and remove `<REMOVE_ME>` in the uncommitted edit.
3. Attempt **Commit changes** on this branch. Confirm the secret-protection block and record redacted evidence.
4. Do not select **Allow secret**, **It's used in tests**, or another bypass. Replace the uncommitted contents with:

   ```text
   TRAINING_VALUE_REMOVED
   ```

5. Retry **Commit changes** and verify the clean commit succeeds. The blocked commit was not created, so there is no terminal commit to amend. This fallback does not prove terminal history repair.

## If detection fails

If the attempt succeeds instead of being blocked, stop. Record **incomplete: no protection block** and keep the nonfunctional branch unmerged. Ask the organizer to check the supported pattern, repository settings, and whether the value was already detected there. Do not try a real credential. If a real secret was used accidentally, revoke or rotate it immediately and follow your incident process.

The [fixture record](fixtures/secret-validation.md) includes the author's earlier local-terminal rejection and clean retry. It does not verify Codespaces, the file editor, or your result. Use the [evidence examples](fixtures/evidence-examples.md) to interpret the fields; they contain no successful scans. Watching a recording leaves your individual outcome incomplete.

## Checkpoint

Record Codespaces, local Git, or file-editor fallback explicitly, with the actual block and clean retry. Explain why deleting a real secret is not sufficient response: revoke or rotate it, assess use, coordinate history cleanup, and prevent recurrence. Codespaces/local Git also demonstrate unpublished-commit repair; the file editor does not.

## Resources

[Supported secret patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns), [blocked terminal pushes](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line), and [blocked web commits](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-in-the-github-ui). Their bypass options are not used in this workshop.

| [Previous: dependencies](4-dependencies.md) | [Next: merge policy](6-merge-policy.md) |
|:---|---:|
