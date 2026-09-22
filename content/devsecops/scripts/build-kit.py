#!/usr/bin/env python3
"""Build a deterministic local companion archive; never publish or change Git."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

KIT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_files():
    return sorted(path for path in KIT.rglob("*")
                  if path.is_file() and "__pycache__" not in path.parts
                  and path.name != ".DS_Store")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--refresh-manifest", action="store_true")
    parser.add_argument("--source-repo", type=Path)
    parser.add_argument("--publication-repo")
    parser.add_argument("--publication-ref")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == KIT or KIT in output.parents:
        parser.error("Archive output must be outside the kit.")
    manifest_path = KIT / "workshop-kit.json"
    manifest = json.loads(manifest_path.read_text())
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", manifest["version"]):
        parser.error("Unsafe kit version.")
    if bool(args.publication_repo) != bool(args.publication_ref):
        parser.error("Provide both publication repository and full commit SHA, or neither.")
    if args.publication_repo:
        if (not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", args.publication_repo)
                or not re.fullmatch(r"[0-9a-f]{40}", args.publication_ref)):
            parser.error("Use owner/repo and a full 40-character commit SHA.")
        if args.publication_repo.lower() == manifest["source_repository"].lower():
            parser.error("Use an authorized companion repository, never upstream.")
    if args.refresh_manifest:
        if not args.source_repo:
            parser.error("--refresh-manifest requires --source-repo.")
        def original(path):
            return subprocess.check_output(
                ["git", "-C", str(args.source_repo), "show", manifest["source_commit"] + ":" + path])
        manifest["fingerprints"] = {
            path: digest(original(path).replace(b"\r\n", b"\n"))
            for path in manifest["baseline_paths"]
        }
        (KIT / "baseline.sha256").write_text("".join(
            f"{checksum}  {path}\n" for path, checksum in manifest["fingerprints"].items()))
        (KIT / "SOURCE-LICENSE").write_bytes(original("LICENSE"))
        manifest["inventory"] = {
            str(path.relative_to(KIT)): digest(path.read_bytes())
            for path in source_files() if path != manifest_path
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    actual = {str(path.relative_to(KIT)): digest(path.read_bytes())
              for path in source_files() if path != manifest_path}
    if actual != manifest["inventory"] or not manifest["fingerprints"]:
        parser.error("Manifest is stale or incomplete; review changes, then refresh it explicitly.")
    output.mkdir(parents=True, exist_ok=True)
    basename = "devsecops-workshop-kit-" + manifest["version"]
    archive = output / (basename + ".zip")
    entries = {str(path.relative_to(KIT)): path.read_bytes() for path in source_files()}
    if args.publication_repo:
        root = f"https://github.com/{args.publication_repo}/blob/{args.publication_ref}"
        raw = f"https://raw.githubusercontent.com/{args.publication_repo}/{args.publication_ref}"
        entries["publication.json"] = (json.dumps({
            "status": "planned-links-not-published-or-verified",
            "repository": args.publication_repo,
            "commit": args.publication_ref,
            "guide": root + "/README.md",
            "ci": raw + "/starter/ci.yml",
            "dependency_review": raw + "/starter/dependency-review.yml",
        }, indent=2) + "\n").encode()
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for path, content in sorted(entries.items()):
            info = ZipInfo(basename + "/" + path, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if path.endswith(".sh") else 0o100644) << 16
            bundle.writestr(info, content)
    checksum = digest(archive.read_bytes())
    archive.with_suffix(".zip.sha256").write_text(f"{checksum}  {archive.name}\n")
    print(archive)
    print("SHA-256:", checksum)
    print("Local archive only. Live evidence and publication remain separate acceptance gates.")


if __name__ == "__main__":
    main()
