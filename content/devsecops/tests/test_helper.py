"""Run only in self-created temporary repositories; never push or access a service."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("PETS_SOURCE_REPO", KIT.parents[1]))
MANIFEST = json.loads((KIT / "workshop-kit.json").read_text())
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
BASH = os.environ.get("WORKSHOP_BASH", "bash")


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=ENV,
                                   stderr=subprocess.STDOUT)


def snapshot(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file() and not path.is_symlink()}


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pets-helper-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "learner with spaces"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "--initial-branch=main")
        git(self.repo, "config", "user.name", "Disposable Test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "core.autocrlf", "false")
        for path in MANIFEST["baseline_paths"]:
            destination = self.repo / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(git(SOURCE, "show", MANIFEST["source_commit"] + ":" + path))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "Disposable template with independent history")
        git(self.repo, "remote", "add", "origin", "https://github.com/learner/pets-training.git")

    def run_helper(self, mode="--apply", ok=True, extra=()):
        before = snapshot(self.repo)
        result = subprocess.run([BASH, (KIT / "scripts/prepare-devsecops.sh").as_posix(),
                                 "--repo", self.repo.as_posix(), mode, *extra],
                                env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        if not ok or mode == "--check":
            self.assertEqual(before, snapshot(self.repo), result.stdout + result.stderr)
        return result

    def install_and_commit(self):
        self.run_helper()
        git(self.repo, "add", ".github/workflows")
        git(self.repo, "commit", "-qm", "Install test workflows")

    def test_check_is_read_only_and_apply_copies_only_two_files(self):
        result = self.run_helper("--check")
        self.assertIn("WOULD COPY .github/workflows/ci.yml", result.stdout)
        before = snapshot(self.repo)
        self.run_helper()
        after = snapshot(self.repo)
        self.assertEqual(set(after) - set(before),
                         {".github/workflows/ci.yml", ".github/workflows/dependency-review.yml"})
        self.assertTrue(all(after[path] == value for path, value in before.items()))
        for name in MANIFEST["core_workflows"]:
            self.assertEqual((self.repo / ".github/workflows" / name).read_bytes(),
                             (KIT / "starter" / name).read_bytes())
        self.run_helper()
        self.assertEqual(after, snapshot(self.repo))

    def test_identical_staged_and_committed_reruns(self):
        self.run_helper()
        git(self.repo, "add", ".github/workflows")
        self.run_helper()
        git(self.repo, "commit", "-qm", "Workflows")
        before = snapshot(self.repo)
        self.run_helper()
        self.assertEqual(before, snapshot(self.repo))

    def test_independent_history_and_crlf(self):
        for path in MANIFEST["baseline_paths"]:
            file = self.repo / path
            file.write_bytes(file.read_bytes().replace(b"\n", b"\r\n"))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "Windows checkout text")
        self.install_and_commit()
        for name in MANIFEST["core_workflows"]:
            file = self.repo / ".github/workflows" / name
            file.write_bytes(file.read_bytes().replace(b"\n", b"\r\n"))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "Windows workflows")
        self.run_helper()

    def test_upstream_and_unsafe_origins(self):
        for origin in ("https://github.com/github-samples/pets-workshop.git",
                       "git@github.com:GitHub-Samples/Pets-Workshop.git",
                       "ssh://git@github.com/github-samples/pets-workshop.git",
                       "https://token@github.com/learner/pets.git", "/tmp/not-a-remote",
                       "https://github.com.evil.invalid/learner/pets"):
            with self.subTest(origin=origin):
                git(self.repo, "remote", "set-url", "origin", origin)
                self.run_helper(ok=False)

    def test_upstream_push_origin(self):
        git(self.repo, "remote", "set-url", "--push", "origin",
            "git@github.com:github-samples/pets-workshop.git")
        self.run_helper(ok=False)

    def test_multiple_origins(self):
        git(self.repo, "remote", "set-url", "--add", "origin", "https://github.com/learner/other")
        self.run_helper(ok=False)

    def test_ssh_learner_origin(self):
        git(self.repo, "remote", "set-url", "origin", "ssh://git@github.com/learner/pets.git")
        self.run_helper()

    def test_missing_origin(self):
        git(self.repo, "remote", "remove", "origin")
        self.run_helper(ok=False)

    def test_wrong_branch_and_detached_head(self):
        git(self.repo, "switch", "-qc", "exercise/not-main")
        self.run_helper(ok=False)
        git(self.repo, "checkout", "-q", "--detach")
        self.run_helper(ok=False)

    def test_untracked_and_staged_unrelated_work(self):
        (self.repo / "notes.txt").write_text("Keep this work\n")
        self.run_helper(ok=False)
        git(self.repo, "add", "notes.txt")
        self.run_helper(ok=False)

    def test_renamed_workflow(self):
        self.install_and_commit()
        git(self.repo, "mv", ".github/workflows/ci.yml", ".github/workflows/old.yml")
        self.run_helper(ok=False)

    def test_incompatible_and_missing_baseline(self):
        path = self.repo / "app/server/app.py"
        path.write_text(path.read_text().replace("debug=True", "debug=False"))
        self.run_helper(ok=False)
        path.unlink()
        self.run_helper(ok=False)

    def test_conflict_is_detected_before_any_copy(self):
        directory = self.repo / ".github/workflows"
        directory.mkdir(parents=True)
        (directory / "dependency-review.yml").write_text("name: Preserve me\n")
        self.run_helper(ok=False)
        self.assertFalse((directory / "ci.yml").exists())

    def test_conflicting_index_even_if_worktree_matches(self):
        self.install_and_commit()
        path = self.repo / ".github/workflows/ci.yml"
        original = path.read_bytes()
        path.write_text("name: Different staged work\n")
        git(self.repo, "add", ".github/workflows/ci.yml")
        path.write_bytes(original)
        self.run_helper(ok=False)

    def test_workflow_deletion(self):
        self.install_and_commit()
        git(self.repo, "rm", ".github/workflows/ci.yml")
        self.run_helper(ok=False)

    def test_symlink_directories_and_files(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.repo / ".github").symlink_to(outside, target_is_directory=True)
        self.run_helper(ok=False)
        self.assertEqual(list(outside.iterdir()), [])
        (self.repo / ".github").unlink()
        directory = self.repo / ".github/workflows"
        directory.mkdir(parents=True)
        (directory / "ci.yml").symlink_to(KIT / "starter/ci.yml")
        self.run_helper(ok=False)

    def test_ignored_workflow(self):
        (self.repo / ".gitignore").write_text(".github/workflows/\n")
        git(self.repo, "add", ".gitignore")
        git(self.repo, "commit", "-qm", "Ignore workflows")
        self.run_helper(ok=False)

    def test_in_progress_merge(self):
        head = git(self.repo, "rev-parse", "HEAD")
        (self.repo / ".git/MERGE_HEAD").write_bytes(head)
        self.run_helper(ok=False)

    def test_argument_errors(self):
        self.run_helper(ok=False, extra=("--check",))
        self.run_helper(ok=False, extra=("--unknown",))
        self.run_helper(ok=False, extra=("--repo", str(self.repo)))

    def test_nested_path_and_non_repository(self):
        for target in (self.repo / "app", self.root):
            result = subprocess.run([BASH, (KIT / "scripts/prepare-devsecops.sh").as_posix(),
                                     "--repo", target.as_posix(), "--check"],
                                    env=ENV, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
