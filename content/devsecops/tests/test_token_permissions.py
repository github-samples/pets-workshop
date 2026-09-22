import contextlib
from email.message import Message
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import yaml

KIT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.load((KIT / "starter/token-permissions.yml").read_text(), Loader=yaml.BaseLoader)
SCRIPT = WORKFLOW["jobs"]["deny-issue-write"]["steps"][0]["run"]
ENV = {
    "GITHUB_EVENT_NAME": "workflow_dispatch",
    "GITHUB_REF": "refs/heads/main",
    "GITHUB_SERVER_URL": "https://github.com",
    "GITHUB_API_URL": "https://api.github.com",
    "GITHUB_REPOSITORY": "learner/pets",
    "GITHUB_RUN_ID": "123",
    "GITHUB_RUN_ATTEMPT": "1",
    "GITHUB_SHA": "a" * 40,
    "GH_TOKEN": "unit-test-token-never-print",
}


class Response(io.BytesIO):
    def __init__(self, status, data, headers=None):
        super().__init__(json.dumps(data).encode() if not isinstance(data, bytes) else data)
        self.code = status
        self.headers = Message()
        for name, value in (headers or {}).items():
            self.headers[name] = value


class TokenPermissionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="pets-token-proof-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.calls = []
        self.stdout = io.StringIO()
        self.metadata = (200, {"has_issues": True, "archived": False})

    def issue(self, mode="allow", state="open", **changes):
        data = {
            "number": 17,
            "title": f"[workshop-token-permissions] 123/1 {mode}",
            "body": ("Harmless workload-identity training issue; close after this exercise.\n\n"
                     "Run: https://github.com/learner/pets/actions/runs/123\n"
                     f"Marker: workshop-token-permissions:123:1:{mode}\n"),
            "user": {"login": "github-actions[bot]", "type": "Bot"},
            "state": state,
        }
        return data | changes

    def execute(self, responses, mode="deny", phase="prove", environment=None):
        replies = iter(responses)

        def open_request(request, timeout):
            self.assertEqual(timeout, 30)
            self.assertTrue(request.full_url.startswith("https://api.github.com/repos/learner/pets"))
            payload = json.loads(request.data) if request.data else None
            self.calls.append((request.method, request.full_url, payload))
            reply = next(replies)
            if isinstance(reply, BaseException):
                raise reply
            return Response(*reply)

        env = ENV | {"RUNNER_TEMP": str(self.root), "GITHUB_STEP_SUMMARY": str(self.root / "summary"),
                     "PROOF_MODE": mode, "PROOF_PHASE": phase} | (environment or {})
        with patch.dict(os.environ, env, clear=True):
            with patch("urllib.request.OpenerDirector.open", side_effect=open_request):
                with contextlib.redirect_stdout(self.stdout):
                    exec(compile(SCRIPT, "inline-token-permission-proof", "exec"), {})
        self.assertNotIn(ENV["GH_TOKEN"], self.stdout.getvalue())

    def test_manual_two_job_least_privilege_contract(self):
        self.assertEqual(set(WORKFLOW["on"]), {"workflow_dispatch"})
        self.assertFalse(WORKFLOW["on"]["workflow_dispatch"])
        self.assertEqual(WORKFLOW["permissions"], {})
        self.assertEqual(set(WORKFLOW["jobs"]), {"deny-issue-write", "allow-issue-write"})
        for name, permission in (("deny-issue-write", "read"), ("allow-issue-write", "write")):
            job = WORKFLOW["jobs"][name]
            self.assertEqual(job["permissions"], {"issues": permission})
            self.assertEqual(job["runs-on"], "ubuntu-24.04")
            self.assertEqual(job["steps"][1]["if"], "always()")
            self.assertEqual(job["steps"][1]["run"], SCRIPT)
            self.assertTrue(all("uses" not in step and "continue-on-error" not in step
                                for step in job["steps"]))
        self.assertEqual(WORKFLOW["jobs"]["allow-issue-write"]["needs"], "deny-issue-write")
        self.assertEqual(WORKFLOW["concurrency"]["cancel-in-progress"], "false")

    def test_exact_non_rate_limited_403_is_expected_denial(self):
        self.execute([self.metadata, (403, {"message": "Resource not accessible by integration"},
                                      {"X-RateLimit-Remaining": "4999"})])
        self.assertIn("Expected denial confirmed", self.stdout.getvalue())
        self.assertFalse((self.root / "workshop-token-deny.json").exists())
        self.assertEqual([call[0] for call in self.calls], ["GET", "POST"])
        self.execute([], phase="cleanup")

    def test_http_error_403_uses_same_narrow_classifier(self):
        headers = Message()
        headers["X-RateLimit-Remaining"] = "42"
        error = urllib.error.HTTPError("https://api.github.com/repos/learner/pets/issues",
                                       403, "Forbidden", headers,
                                       io.BytesIO(b'{"message":"Resource not accessible by integration"}'))
        self.execute([self.metadata, error])
        self.assertIn("Expected denial confirmed", self.stdout.getvalue())

    def test_other_statuses_are_not_denial_proof(self):
        for status in (200, 302, 401, 404, 410, 422, 429, 500):
            with self.subTest(status=status), self.assertRaises(SystemExit):
                self.execute([self.metadata, (status, {"message": "Resource not accessible by integration"},
                                               {"X-RateLimit-Remaining": "4"})])

    def test_other_403_causes_and_rate_limits_fail(self):
        cases = [
            ({"message": "API rate limit exceeded"}, {"X-RateLimit-Remaining": "0"}),
            ({"message": "Resource not accessible by integration"}, {"X-RateLimit-Remaining": "0"}),
            ({"message": "Resource not accessible by integration"}, {"X-RateLimit-Remaining": "4", "Retry-After": "60"}),
            ({"message": "Resource not accessible by integration"}, {}),
            ({"message": "Forbidden by policy"}, {"X-RateLimit-Remaining": "4"}),
        ]
        for data, headers in cases:
            with self.subTest(data=data, headers=headers), self.assertRaises(SystemExit):
                self.execute([self.metadata, (403, data, headers)])

    def test_disabled_issues_archived_or_bad_preflight_never_posts(self):
        for metadata in ((200, {"has_issues": False, "archived": False}),
                         (200, {"has_issues": True, "archived": True}), (404, {}), (401, {})):
            self.calls.clear()
            with self.subTest(metadata=metadata), self.assertRaises(SystemExit):
                self.execute([metadata])
            self.assertEqual([call[0] for call in self.calls], ["GET"])

    def test_network_failure_is_not_retried_or_counted(self):
        for failure in (urllib.error.URLError("connection failed"), TimeoutError()):
            self.calls.clear()
            with self.subTest(failure=failure), self.assertRaisesRegex(SystemExit, "Network failure"):
                self.execute([self.metadata, failure])
            self.assertEqual([call[0] for call in self.calls], ["GET", "POST"])
            self.assertIn("Recovery search:", self.stdout.getvalue())

    def test_bad_json_or_missing_number_fails_without_false_proof(self):
        for response in ((403, b"not json"), (403, []), (201, {"number": True}),
                         (201, {"number": -1}), (201, {})):
            with self.subTest(response=response), self.assertRaises(SystemExit):
                self.execute([self.metadata, response])

    def test_non_main_or_nonmanual_never_accesses_network(self):
        for environment in ({"GITHUB_REF": "refs/heads/exercise/token"},
                            {"GITHUB_REF": "refs/tags/main"},
                            {"GITHUB_EVENT_NAME": "pull_request"}):
            for phase in ("prove", "cleanup"):
                with self.subTest(environment=environment, phase=phase), self.assertRaises(SystemExit):
                    self.execute([], phase=phase, environment=environment)
        self.assertEqual(self.calls, [])

    def test_allow_records_bot_issue_and_cleanup_closes_only_that_issue(self):
        issue = self.issue()
        self.execute([self.metadata, (201, issue)], mode="allow")
        self.assertIn("actual creator: github-actions[bot]", self.stdout.getvalue())
        self.assertIn("https://github.com/learner/pets/issues/17", self.stdout.getvalue())
        self.execute([(200, issue), (200, self.issue(state="closed"))], mode="allow", phase="cleanup")
        self.assertEqual(self.calls[-1],
                         ("PATCH", "https://api.github.com/repos/learner/pets/issues/17", {"state": "closed"}))
        self.assertIn("Confirmed closed:", self.stdout.getvalue())

    def test_unexpected_deny_success_remains_failed_after_cleanup(self):
        issue = self.issue(mode="deny")
        with self.assertRaisesRegex(SystemExit, "denial proof FAILED"):
            self.execute([self.metadata, (201, issue)])
        self.execute([(200, issue), (200, self.issue(mode="deny", state="closed"))], phase="cleanup")
        self.assertIn("Confirmed closed:", self.stdout.getvalue())
        self.assertNotIn("Expected denial confirmed", self.stdout.getvalue())

    def test_bad_creation_assertion_still_records_cleanup_target(self):
        with self.assertRaisesRegex(SystemExit, "Issue identity"):
            self.execute([self.metadata, (201, self.issue(user={"login": "unexpected"}))], mode="allow")
        self.assertTrue((self.root / "workshop-token-allow.json").exists())
        self.assertIn("/issues/17", self.stdout.getvalue())

    def test_cleanup_refuses_other_issue_and_pr_identities(self):
        self.execute([self.metadata, (201, self.issue())], mode="allow")
        for changes in ({"title": "Unrelated"}, {"body": "Other run"}, {"pull_request": {}},
                        {"number": 18}, {"user": {"login": "octocat", "type": "User"}}):
            self.calls.clear()
            with self.subTest(changes=changes), self.assertRaisesRegex(SystemExit, "Issue identity"):
                self.execute([(200, self.issue(**changes))], mode="allow", phase="cleanup")
            self.assertEqual([call[0] for call in self.calls], ["GET"])

    def test_cleanup_failures_report_exact_manual_recovery_url(self):
        self.execute([self.metadata, (201, self.issue())], mode="allow")
        for responses in ([(404, {})], [(200, self.issue()), (403, {})],
                          [(200, self.issue()), (200, self.issue())]):
            with self.subTest(responses=responses), self.assertRaisesRegex(SystemExit, "/issues/17"):
                self.execute(responses, mode="allow", phase="cleanup")

    def test_already_closed_cleanup_is_idempotent(self):
        self.execute([self.metadata, (201, self.issue())], mode="allow")
        self.calls.clear()
        self.execute([(200, self.issue(state="closed"))], mode="allow", phase="cleanup")
        self.assertEqual([call[0] for call in self.calls], ["GET"])

    def test_allow_cannot_claim_permission_failure_as_success(self):
        with self.assertRaisesRegex(SystemExit, "Authorized creation expected HTTP 201"):
            self.execute([self.metadata, (403, {"message": "Resource not accessible by integration"},
                                         {"X-RateLimit-Remaining": "42"})], mode="allow")

    def test_cleanup_rejects_foreign_run_state_before_network(self):
        (self.root / "workshop-token-allow.json").write_text(
            json.dumps({"repository": "other/repo", "title": "Other", "number": 17}))
        with self.assertRaisesRegex(SystemExit, "does not belong"):
            self.execute([], mode="allow", phase="cleanup")
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
