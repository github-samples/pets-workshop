#!/usr/bin/env bash
set -euo pipefail
export GIT_OPTIONAL_LOCKS=0

fail() {
    printf 'ERROR: %s\nRecovery: see 0-setup.md and take-home/troubleshooting.md in this kit.\n' "$*" >&2
    exit 1
}

usage() {
    printf 'Usage: bash prepare-devsecops.sh --repo PATH (--check | --apply)\n'
}

repo=
mode=
while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)
            [[ $# -ge 2 && -z "$repo" && -n "$2" ]] || fail "Supply --repo once with a path."
            repo=$2
            shift 2
            ;;
        --check|--apply)
            [[ -z "$mode" ]] || fail "Choose exactly one of --check and --apply."
            mode=$1
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *) fail "Unknown argument: $1" ;;
    esac
done
[[ -n "$repo" && -n "$mode" ]] || { usage >&2; exit 1; }
command -v git >/dev/null || fail "Git is required for this optional route; use the web route instead."
kit=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
[[ -d "$repo" ]] || fail "Repository directory does not exist."
repo=$(cd "$repo" && pwd -P)
[[ "$(git -C "$repo" rev-parse --is-inside-work-tree 2>/dev/null)" == true ]] ||
    fail "Target is not a Git working tree."
root=$(git -C "$repo" rev-parse --show-toplevel)
[[ "$repo" == "$(cd "$root" && pwd -P)" ]] || fail "--repo must name the repository root."
[[ "$(git -C "$repo" symbolic-ref --short -q HEAD)" == main ]] ||
    fail "Switch to your prepared main without discarding work."
git_dir=$(git -C "$repo" rev-parse --absolute-git-dir)
for state in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD rebase-merge rebase-apply; do
    [[ ! -e "$git_dir/$state" ]] ||
        fail "Finish or safely abort the existing Git operation before setup."
done

normalize_origin() {
    local url
    url=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
    case "$url" in
        https://github.com/*) url=${url#https://github.com/} ;;
        git@github.com:*) url=${url#git@github.com:} ;;
        ssh://git@github.com/*) url=${url#ssh://git@github.com/} ;;
        *) fail "Origin must be a direct GitHub.com learner URL, without credentials or aliases." ;;
    esac
    url=${url%.git}
    [[ "$url" =~ ^[a-z0-9][a-z0-9-]*/[a-z0-9_.-]+$ ]] ||
        fail "Origin must identify exactly one owner/repository."
    [[ "$url" != github-samples/pets-workshop ]] || fail "Refusing the upstream Pets repository."
    printf '%s' "$url"
}
origin=$(git -C "$repo" remote get-url --all origin) || fail "Origin is missing."
push_origin=$(git -C "$repo" remote get-url --push --all origin) || fail "Push origin is missing."
origin=$(normalize_origin "$origin") || fail "Unsafe fetch origin."
push_origin=$(normalize_origin "$push_origin") || fail "Unsafe push origin."
[[ "$origin" == "$push_origin" ]] ||
    fail "Fetch and push origins must name the same learner repository."

if command -v sha256sum >/dev/null; then
    hash_command=(sha256sum)
elif command -v shasum >/dev/null; then
    hash_command=(shasum -a 256)
else
    fail "A SHA-256 tool is required; use the web route instead."
fi
hash_file() {
    # Git Bash may check out CRLF; compare the tested text with LF endings.
    sed 's/\r$//' "$1" | "${hash_command[@]}" | cut -d ' ' -f 1
}
[[ -f "$kit/baseline.sha256" ]] || fail "The kit is incomplete: baseline.sha256 is missing."
fingerprint_count=0
while read -r expected path; do
    path=${path%$'\r'}
    [[ "$expected" =~ ^[0-9a-f]{64}$ && "$path" == app/* && "$path" != *..* ]] ||
        fail "Malformed baseline fingerprint."
    [[ -f "$repo/$path" && ! -L "$repo/$path" ]] || fail "Missing or linked baseline file: $path"
    [[ "$(hash_file "$repo/$path")" == "$expected" ]] ||
        fail "Incompatible baseline: $path. Do not overwrite it; ask for a retested companion kit."
    fingerprint_count=$((fingerprint_count + 1))
done < "$kit/baseline.sha256"
[[ "$fingerprint_count" -eq 9 ]] || fail "The kit must contain all nine tested baseline fingerprints."

for directory in .github .github/workflows; do
    [[ ! -L "$repo/$directory" ]] || fail "Refusing symlink: $directory"
    [[ ! -e "$repo/$directory" || -d "$repo/$directory" ]] || fail "Not a directory: $directory"
done
files=(ci.yml dependency-review.yml)
for file in "${files[@]}"; do
    source_path="$kit/starter/$file"
    target="$repo/.github/workflows/$file"
    [[ -f "$source_path" && ! -L "$source_path" ]] || fail "Missing or linked kit starter: $file"
    [[ ! -L "$target" ]] || fail "Refusing symlink: $target"
    if [[ -e "$target" ]]; then
        [[ -f "$target" && "$(hash_file "$target")" == "$(hash_file "$source_path")" ]] ||
            fail "Conflicting workflow: $file. Review it manually; nothing was copied."
    fi
    if git -C "$repo" check-ignore -q ".github/workflows/$file"; then
        fail "Workflow is ignored by Git: $file"
    fi
done

status=$(git -C "$repo" status --porcelain=v1 --untracked-files=all)
while IFS= read -r entry; do
    [[ -n "$entry" ]] || continue
    path=${entry:3}
    case "$path" in
        .github/workflows/ci.yml|.github/workflows/dependency-review.yml)
            [[ "${entry:0:2}" != *D* && -f "$repo/$path" ]] ||
                fail "Workflow deletion or conflict requires manual recovery."
            if git -C "$repo" ls-files --error-unmatch "$path" >/dev/null 2>&1; then
                indexed=$(git -C "$repo" show ":$path" | sed 's/\r$//' | "${hash_command[@]}" | cut -d ' ' -f 1)
                [[ "$indexed" == "$(hash_file "$kit/starter/${path##*/}")" ]] ||
                    fail "Conflicting staged workflow: $path"
            fi
            ;;
        *) fail "Unrelated change: $path. Commit or move your work yourself; no stash/reset was done." ;;
    esac
done <<< "$status"

for file in "${files[@]}"; do
    target="$repo/.github/workflows/$file"
    if [[ -f "$target" ]]; then
        printf 'UNCHANGED .github/workflows/%s\n' "$file"
    elif [[ "$mode" == --check ]]; then
        printf 'WOULD COPY .github/workflows/%s\n' "$file"
    else
        mkdir -p "$repo/.github/workflows"
        cp "$kit/starter/$file" "$target"
        printf 'COPIED .github/workflows/%s\n' "$file"
    fi
done
printf 'Local %s complete. No commit, push, authentication, or repository setting was changed.\n' "$mode"
