#!/usr/bin/env bash
#
# Reset the demo repository back to the tagged baseline between sessions.
# Discards working-tree changes, removes untracked files, deletes the
# live-authored Copilot instructions, and resets to the demo-baseline tag.
set -euo pipefail

# The canonical upstream repository. The reset is destructive, so refuse to
# run it against upstream on main to avoid pointing it at the wrong repo.
UPSTREAM="github-samples/pets-workshop"
BASELINE_TAG="demo-baseline"

cd "$(git rev-parse --show-toplevel)"

branch="$(git rev-parse --abbrev-ref HEAD)"
origin_url="$(git config --get remote.origin.url || true)"

if [ "$branch" = "main" ] && printf '%s' "$origin_url" | grep -qi "$UPSTREAM"; then
  echo "Refusing to run: origin is the upstream ($UPSTREAM) and the branch is 'main'." >&2
  echo "Point this at your own demo fork before resetting." >&2
  exit 1
fi

if ! git rev-parse -q --verify "refs/tags/${BASELINE_TAG}" >/dev/null; then
  echo "Tag '${BASELINE_TAG}' not found. Create it first (see scripts/README.md)." >&2
  exit 1
fi

echo "Discarding working-tree changes..."
git reset --hard

echo "Removing untracked files..."
git clean -fd

echo "Removing live-authored Copilot instructions (if present)..."
rm -f .github/copilot-instructions.md

echo "Resetting to tag '${BASELINE_TAG}'..."
git reset --hard "${BASELINE_TAG}"

echo "Done. Repository is back at '${BASELINE_TAG}'."
