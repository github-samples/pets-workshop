import shutil
import subprocess
import unittest

import test_helper


class FetchRouteTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_helper.HelperTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_tag_fetch_archive_and_helper_preserve_learner_history(self):
        repo = self.fixture.repo
        root = self.fixture.root
        companion = root / "companion"
        shutil.copytree(test_helper.KIT, companion,
                        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        git = test_helper.git
        git(companion, "init", "-q", "--initial-branch=main")
        git(companion, "config", "user.name", "Disposable Companion")
        git(companion, "config", "user.email", "test@example.invalid")
        git(companion, "add", ".")
        git(companion, "commit", "-qm", "Independent companion root")
        git(companion, "tag", "v0.1.0")
        original_head = git(repo, "rev-parse", "HEAD")
        original_remotes = git(repo, "remote", "-v")
        git(repo, "fetch", "--no-tags", str(companion), "refs/tags/v0.1.0")
        self.assertEqual(git(repo, "rev-parse", "FETCH_HEAD^{commit}"),
                         git(companion, "rev-parse", "HEAD"))
        archive = root / "pets-devsecops-kit-v0.1.0.tar"
        extracted = root / "pets-devsecops-kit-v0.1.0"
        extracted.mkdir()
        git(repo, "archive", "--format=tar", "--output=" + str(archive), "FETCH_HEAD")
        subprocess.run(["tar", "-xf", archive.name, "-C", extracted.name], cwd=root, check=True)
        self.assertTrue((extracted / "starter/ci.yml").exists())
        self.assertTrue((extracted / "take-home/2-approve-a-release.md").exists())
        self.assertFalse((extracted / "content/devsecops").exists())
        self.assertEqual(git(repo, "rev-parse", "HEAD"), original_head)
        self.assertEqual(git(repo, "remote", "-v"), original_remotes)
        self.assertEqual(git(repo, "status", "--porcelain"), b"")
        unrelated = subprocess.run(["git", "-C", str(repo), "merge-base", "HEAD", "FETCH_HEAD"],
                                   env=test_helper.ENV, capture_output=True)
        self.assertEqual(unrelated.returncode, 1)
        for mode in ("--check", "--apply"):
            result = subprocess.run(
                [test_helper.BASH, (extracted / "scripts/prepare-devsecops.sh").as_posix(),
                 "--repo", repo.as_posix(), mode], env=test_helper.ENV,
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(git(repo, "rev-parse", "HEAD"), original_head)
        self.assertEqual(git(repo, "remote", "-v"), original_remotes)
        self.assertEqual(
            (repo / ".github/workflows/ci.yml").read_bytes(),
            (test_helper.KIT / "starter/ci.yml").read_bytes())

    def test_empty_fingerprint_inventory_refuses_without_changes(self):
        copy = self.fixture.root / "incomplete-kit"
        shutil.copytree(test_helper.KIT, copy, ignore=shutil.ignore_patterns("__pycache__"))
        (copy / "baseline.sha256").write_text("")
        before = test_helper.snapshot(self.fixture.repo)
        result = subprocess.run(
            [test_helper.BASH, (copy / "scripts/prepare-devsecops.sh").as_posix(), "--repo",
             self.fixture.repo.as_posix(), "--apply"], env=test_helper.ENV, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, test_helper.snapshot(self.fixture.repo))

    def test_crlf_fingerprint_manifest_preserves_validation(self):
        copy = self.fixture.root / "crlf-kit"
        shutil.copytree(test_helper.KIT, copy, ignore=shutil.ignore_patterns("__pycache__"))
        fingerprints = copy / "baseline.sha256"
        fingerprints.write_bytes(fingerprints.read_bytes().replace(b"\r\n", b"\n")
                                 .replace(b"\n", b"\r\n"))
        command = [test_helper.BASH, (copy / "scripts/prepare-devsecops.sh").as_posix(),
                   "--repo", self.fixture.repo.as_posix()]
        before = test_helper.snapshot(self.fixture.repo)
        check = subprocess.run(command + ["--check"], env=test_helper.ENV,
                               capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(before, test_helper.snapshot(self.fixture.repo))
        applied = subprocess.run(command + ["--apply"], env=test_helper.ENV,
                                 capture_output=True, text=True)
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        path = self.fixture.repo / "app/client/package.json"
        path.write_bytes(path.read_bytes() + b"\n")
        changed = test_helper.snapshot(self.fixture.repo)
        rejected = subprocess.run(command + ["--apply"], env=test_helper.ENV, capture_output=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(changed, test_helper.snapshot(self.fixture.repo))


if __name__ == "__main__":
    unittest.main()
