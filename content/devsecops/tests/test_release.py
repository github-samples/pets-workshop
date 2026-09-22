import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error
from urllib.parse import urlsplit

import yaml

KIT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.load((KIT / "starter/release-simulation.yml").read_text(), Loader=yaml.BaseLoader)
GUARD = WORKFLOW["jobs"]["guard"]["steps"][0]["run"]
SHA = "a" * 40
ENV = {
    "GITHUB_REF": "refs/heads/main",
    "GITHUB_EVENT_NAME": "workflow_dispatch",
    "GITHUB_API_URL": "https://api.example.invalid",
    "GITHUB_REPOSITORY": "learner/pets",
    "GITHUB_SHA": SHA,
    "GH_TOKEN": "unit-test-placeholder",
}


class ReleaseGuardTests(unittest.TestCase):
    def setUp(self):
        self.responses = {
            "/git/ref/heads/main": {"object": {"sha": SHA}},
            "/environments/workshop-demo": {
                "can_admins_bypass": False,
                "protection_rules": [{"type": "required_reviewers", "reviewers": [{"id": 1}]}],
                "deployment_branch_policy": {
                    "protected_branches": False, "custom_branch_policies": True},
            },
            "/environments/workshop-demo/deployment-branch-policies": {
                "total_count": 1, "branch_policies": [{"name": "main", "type": "branch"}]},
        }

    def execute(self, env=None, responses=None):
        data = self.responses if responses is None else responses
        def urlopen(request, timeout):
            self.assertEqual(timeout, 30)
            path = urlsplit(request.full_url).path.removeprefix("/repos/learner/pets")
            if path not in data:
                raise urllib.error.HTTPError(request.full_url, 404, "Not found", None, io.BytesIO())
            return io.StringIO(json.dumps(data[path]))
        with patch.dict(os.environ, ENV | (env or {}), clear=True):
            with patch("urllib.request.urlopen", side_effect=urlopen):
                exec(compile(GUARD, "release-inline-guard", "exec"), {})

    def test_current_main_push_and_dispatch_pass(self):
        self.execute()
        self.execute({"GITHUB_EVENT_NAME": "push"})

    def test_non_main_and_pr_events_fail(self):
        for env in ({"GITHUB_REF": "refs/heads/exercise/release"},
                    {"GITHUB_REF": "refs/tags/main"},
                    {"GITHUB_EVENT_NAME": "pull_request"}):
            with self.subTest(env=env), self.assertRaises(SystemExit):
                self.execute(env)

    def test_stale_revision_fails(self):
        with self.assertRaisesRegex(SystemExit, "Stale revision"):
            self.execute({"GITHUB_SHA": "b" * 40})

    def test_missing_environment_or_api_failure_fails(self):
        del self.responses["/environments/workshop-demo"]
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.execute()
        raised.exception.close()

    def test_missing_or_empty_reviewers_fail(self):
        for rules in ([], [{"type": "required_reviewers", "reviewers": []}]):
            with self.subTest(rules=rules):
                self.responses["/environments/workshop-demo"]["protection_rules"] = rules
                with self.assertRaisesRegex(SystemExit, "required reviewers"):
                    self.execute()

    def test_admin_bypass_fails(self):
        self.responses["/environments/workshop-demo"]["can_admins_bypass"] = True
        with self.assertRaisesRegex(SystemExit, "administrator bypass"):
            self.execute()

    def test_unrestricted_and_protected_branch_modes_fail(self):
        for policy in (None, {}, {"protected_branches": True, "custom_branch_policies": False}):
            with self.subTest(policy=policy):
                self.responses["/environments/workshop-demo"]["deployment_branch_policy"] = policy
                with self.assertRaisesRegex(SystemExit, "selected branches"):
                    self.execute()

    def test_wildcard_tag_extra_and_missing_branch_rules_fail(self):
        for branches in (
                {"total_count": 0, "branch_policies": []},
                {"total_count": 1, "branch_policies": [{"name": "*", "type": "branch"}]},
                {"total_count": 1, "branch_policies": [{"name": "main", "type": "tag"}]},
                {"total_count": 2, "branch_policies": [{"name": "main", "type": "branch"}]}):
            with self.subTest(branches=branches):
                self.responses["/environments/workshop-demo/deployment-branch-policies"] = branches
                with self.assertRaisesRegex(SystemExit, "Only the main branch"):
                    self.execute()

    def test_same_guard_repeats_after_approval(self):
        self.assertEqual(WORKFLOW["jobs"]["release"]["steps"][0]["run"], GUARD)
        self.execute()
        self.responses["/git/ref/heads/main"]["object"]["sha"] = "b" * 40
        with self.assertRaisesRegex(SystemExit, "Stale revision"):
            self.execute()


if __name__ == "__main__":
    unittest.main()
