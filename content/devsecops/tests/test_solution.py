import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("PETS_SOURCE_REPO", KIT.parents[1]))


class SolutionTests(unittest.TestCase):
    def test_regression_is_red_before_and_green_after(self):
        with tempfile.TemporaryDirectory(prefix="pets-startup-test-") as temporary:
            server = Path(temporary) / "server"
            shutil.copytree(SOURCE / "app/server", server,
                            ignore=shutil.ignore_patterns("__pycache__", "*.db"))
            tests = server / "test_app.py"
            tests.write_text(tests.read_text().replace(
                "\nif __name__ == '__main__':",
                "\n" + (KIT / "solutions/startup-test.py.txt").read_text()
                + "\nif __name__ == '__main__':"))
            env = dict(os.environ, DATABASE_PATH=":memory:", PYTHONDONTWRITEBYTECODE="1")
            command = [sys.executable, "-m", "unittest", "test_app", "-v"]
            before = subprocess.run(command, cwd=server, env=env, capture_output=True, text=True)
            self.assertNotEqual(before.returncode, 0)
            self.assertIn("AssertionError", before.stderr)
            self.assertIn("debug=True", before.stderr)
            self.assertIn("Ran 4 tests", before.stderr)
            app = server / "app.py"
            original = app.read_text()
            self.assertEqual(original.count("app.run(debug=True, port=5100)"), 1)
            app.write_text(original.replace("app.run(debug=True, port=5100)",
                                            "app.run(debug=False, port=5100)"))
            after = subprocess.run(command, cwd=server, env=env, capture_output=True, text=True)
            self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
            self.assertIn("Ran 4 tests", after.stderr)


if __name__ == "__main__":
    unittest.main()
