#!/usr/bin/env python3
"""Check local links, snippets, workflow contracts and fixture safety without networking."""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import textwrap
from urllib.parse import unquote, urlsplit

import yaml

KIT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def headings(text):
    counts = {}
    anchors = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        base = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(base, 0)
        anchors.add(base + (f"-{count}" if count else ""))
        counts[base] = count + 1
    return anchors


def main():
    markdown = sorted(KIT.rglob("*.md"))
    require(markdown, "No Markdown files found")
    link_count = 0
    snippets = 0
    for file in markdown:
        text = file.read_text()
        require("Why it matters" in text, f"{file}: missing lesson purpose")
        require("checkpoint" in text.lower(), f"{file}: missing observable checkpoint")
        require("https://" in text, f"{file}: missing external reference")
        without_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        targets = re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", without_code)
        targets += re.findall(r"^\[[^\]]+\]:\s+(\S+)", without_code, re.MULTILINE)
        for target in targets:
            parts = urlsplit(target)
            if parts.scheme:
                require(parts.scheme in ("https", "mailto"), f"Unsupported link: {target}")
                continue
            destination = (file.parent / unquote(parts.path)).resolve() if parts.path else file
            require(destination == KIT or KIT in destination.parents,
                    f"{file}: relative link escapes companion kit: {target}")
            require(destination.exists(), f"{file}: missing target {target}")
            if parts.fragment and destination.suffix == ".md":
                require(unquote(parts.fragment) in headings(destination.read_text()),
                        f"{file}: missing heading {target}")
            link_count += 1
        for language, content in re.findall(r"```([a-z]*)\n(.*?)```", text, re.DOTALL):
            if language == "bash":
                subprocess.run(["bash", "-n"], input=content, text=True, check=True)
                snippets += 1
            elif language == "python":
                ast.parse(textwrap.dedent(content))
                snippets += 1
            elif language in ("yaml", "json"):
                yaml.load(content, Loader=yaml.BaseLoader)
                snippets += 1
    workflows = {name: yaml.load((KIT / "starter" / name).read_text(), Loader=yaml.BaseLoader)
                 for name in ("ci.yml", "dependency-review.yml", "release-simulation.yml")}
    for name, workflow in workflows.items():
        require(workflow["permissions"] == {"contents": "read"}, f"{name}: unexpected permission")
        require("pull_request_target" not in workflow["on"], f"{name}: privileged PR trigger")
        require(not re.search(r"paths(?:-ignore)?:", (KIT / "starter" / name).read_text()),
                f"{name}: required workflow can be skipped by paths")
        for job in workflow["jobs"].values():
            require(job["runs-on"] == "ubuntu-24.04", f"{name}: nonstandard runner")
            require(int(job["timeout-minutes"]) <= 10, f"{name}: unbounded job")
            for step in job["steps"]:
                if "uses" in step:
                    require(re.fullmatch(r"actions/[\w-]+@[0-9a-f]{40}", step["uses"]),
                            f"{name}: unpinned action")
                if step.get("uses", "").startswith("actions/checkout@"):
                    require(step["with"]["persist-credentials"] == "false",
                            f"{name}: persisted credential")
                if "run" in step:
                    require("workshop-lab" not in step["run"], f"{name}: fixture execution")
                    if step.get("shell") == "python":
                        ast.parse(step["run"])
                    else:
                        subprocess.run(["bash", "-n"], input=step["run"], text=True, check=True)
    ci = workflows["ci.yml"]
    require(set(ci["jobs"]) == {"api-tests", "client-build"}, "Unstable CI job names")
    require(set(ci["on"]) == {"push", "pull_request", "workflow_dispatch"}, "CI triggers changed")
    review = workflows["dependency-review.yml"]
    require(set(review["jobs"]) == {"dependency-review"}, "Unstable dependency check name")
    require(set(review["on"]) == {"pull_request"}, "Dependency trigger changed")
    review_inputs = review["jobs"]["dependency-review"]["steps"][-1]["with"]
    require(review_inputs["fail-on-severity"] == "high", "Wrong severity")
    require(review_inputs["warn-only"] == "false", "Failure hidden as warning")
    require(set(part.strip() for part in review_inputs["fail-on-scopes"].split(","))
            == {"runtime", "development", "unknown"}, "Incomplete dependency scopes")
    release = workflows["release-simulation.yml"]
    require(set(release["on"]) == {"push", "workflow_dispatch"}, "Release PR trigger")
    job = release["jobs"]["release"]
    require(set(job["needs"]) == {"guard", "release-api-tests", "release-client-build"},
            "Missing release prerequisite")
    for name in job["needs"]:
        require(f"needs.{name}.result == 'success'" in job["if"], "Release is not fail-closed")
    require("!cancelled()" in job["if"], "Cancelled release allowed")
    require(job["environment"] == "workshop-demo", "Wrong release environment")
    require(job["steps"][0] == release["jobs"]["guard"]["steps"][0], "Missing post-approval recheck")
    for name in ("release-api-tests", "release-client-build"):
        require(release["jobs"][name]["steps"][0]["with"]["ref"] == "${{ github.sha }}",
                "Release checkout is not bound to the run SHA")
    def constraints(workflow, name):
        return next(step["run"] for step in workflow["jobs"][name]["steps"]
                    if step.get("name") == "Install workshop Python baseline")
    require(constraints(ci, "api-tests") == constraints(release, "release-api-tests"),
            "Python snapshots diverged")
    require(not (KIT / ".github/workflows").exists(), "Kit has active workflows")
    fixture = (KIT / "fixtures/secret-training.txt").read_text()
    require("<REMOVE_ME>" in fixture and fixture.count("<REMOVE_ME>") == 1, "Fixture not inert")
    for path in KIT.rglob("*"):
        require(not path.is_symlink(), f"Symlink in distributable: {path}")
        if path.is_file() and path.suffix in (".md", ".txt", ".json", ".yml", ".py", ".sh"):
            require(not re.search(r"github_pat_[A-Za-z0-9_]{70,}", path.read_text()),
                    f"Unmasked fixture/token in source: {path}")
    manifest = json.loads((KIT / "workshop-kit.json").read_text())
    require(manifest["core_workflows"] == ["ci.yml", "dependency-review.yml"], "Helper scope changed")
    print(f"Validated {len(markdown)} Markdown files, {link_count} local links, "
          f"{snippets} command/config snippets, and three inert workflows.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, SyntaxError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
