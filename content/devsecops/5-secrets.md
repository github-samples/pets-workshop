# 5. Block a secret before it enters history

| [Previous: dependencies](4-dependencies.md) | [Next: merge policy](6-merge-policy.md) |
|:---|---:|

Budget: 12 minutes. A volunteer pastes a credential while troubleshooting. Each participant's intended outcome is a real protection block and a clean retry.

## Why it matters

A later deletion commit leaves the earlier value in Git history. Push protection can stop supported values before they arrive; a real exposure still requires revocation or rotation and investigation.

> [!WARNING]
> Use only [the supplied delimiter-masked fixture](fixtures/secret-training.txt), which the official GitHub Skills source identifies as inactive. Its terminal block/repair was observed; the fresh browser route still needs rehearsal. Read [the provenance and route status](fixtures/secret-validation.md) before attempting it. Never generate a credential, use an active token, or substitute an invented value to force detection.

## Before the attempt

1. Confirm repository **Secret scanning** and **Push protection** are enabled.
2. Read the fixture record's inactive-source evidence, kit version, supported pattern, route results, and date. The organizer must finish the supported-route rehearsal before presenting this as a verified event exercise.
3. Work on `exercise/secret-protection`, created from prepared `main`, separate from your code and dependency PRs. Do not pre-seed the fixture into the template or any published branch.

## Web route (narrated, only after fixture approval)

1. In your learner repository, use the branch selector to create `exercise/secret-protection` from `main`.
2. Select **Add file > Create new file**. Name the file `secret-training.txt`. Paste the supplied fixture line and remove the literal `<REMOVE_ME>` delimiter in this uncommitted edit only.
3. Select **Commit changes** on this branch. Confirm GitHub blocks the commit and identifies the supported pattern. Record the branch, path, time, and a redacted screenshot; never publish the value itself.
4. Do not select **Allow secret**, **It's used in tests**, or any bypass option. Return to the uncommitted edit and replace its entire contents with:

   ```text
   TRAINING_VALUE_REMOVED
   ```

5. Retry **Commit changes** and confirm it succeeds. Record the clean commit URL. The blocked commit was never created: this route does not involve terminal history repair.

## Terminal route (only after fixture approval)

1. From clean prepared `main`, run:

   ```bash
   git switch main
   git switch -c exercise/secret-protection
   ```

2. In your editor, copy the supplied fixture line into `secret-training.txt` and remove its literal `<REMOVE_ME>` delimiter. Do not change the copy in the kit. Then run:

   ```bash
   git add -- secret-training.txt
   git commit -m "Attempt approved nonfunctional training fixture"
   git push -u origin exercise/secret-protection
   ```

3. Confirm the server blocks the push. Keep the rejection's commit/path evidence with the value redacted. Do not follow a bypass link.
4. For this single, newest, unpublished training commit, replace the file with `TRAINING_VALUE_REMOVED`. Rewrite that unpublished commit, then push normally:

   ```bash
   git add -- secret-training.txt
   git diff --cached
   git commit --amend --no-edit
   git push -u origin exercise/secret-protection
   ```

5. Confirm the clean push succeeds. Do not use force push. Leave the branch unmerged.

The narrow amend above is an explicit part of this exercise. If the rejection lists several affected unpublished commits, editing only the latest one is insufficient. Stop the timed path and follow [the multi-commit recovery](take-home/troubleshooting.md#more-than-one-unpublished-secret-commit), checking every affected commit. Never rewrite someone else's published work.

## If detection fails

If the attempt succeeds instead of being blocked, stop. Record **incomplete: no protection block** and keep the nonfunctional branch unmerged. Ask the organizer to check the supported pattern, repository settings, and whether the value was already detected there. Do not try a real credential. If a real secret was used accidentally, revoke or rotate it immediately and follow your incident process.

The [fixture record](fixtures/secret-validation.md) includes the author's redacted terminal rejection and clean retry. It does not verify the web route or your own result. Use the [evidence examples](fixtures/evidence-examples.md) to interpret the fields; they contain no successful scans. Watching a recording leaves your individual outcome incomplete.

## Checkpoint

Record your route, actual block evidence, and clean retry. Explain why deleting a real secret is not sufficient response: revoke or rotate it, assess use, coordinate history cleanup, and prevent recurrence. The web route proves a blocked commit; the terminal route also proves unpublished-commit repair.

## Resources

[Supported secret patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns), [blocked terminal pushes](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line), and [blocked web commits](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-in-the-github-ui). Their bypass options are not used in this workshop.

| [Previous: dependencies](4-dependencies.md) | [Next: merge policy](6-merge-policy.md) |
|:---|---:|
