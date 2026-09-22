# Technical sources and maintenance

## Why it matters

Action tags, package advisories, and product interfaces change. A versioned kit needs a record of what was checked and a way to update it without guessing.

## Source and runtime baseline

The original Pets source inspected locally and through the GitHub API is [d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a](https://github.com/github-samples/pets-workshop/tree/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a). The live upstream `main` still matched it during the 2026-09-22 UTC check. Template copies have independent Git history; compatibility uses [file fingerprints](baseline.sha256), also recorded in [the manifest](workshop-kit.json).

The only learner application template is the original Pets repository. If it changes incompatibly, update and retest the companion kit. Do not substitute a derived application template.

Standard `ubuntu-24.04` runners use Python 3.14 and Node 24. [Astro 6's upgrade guide](https://docs.astro.build/en/guides/upgrade-to/v6/) requires Node >=22.12. Existing Pets lessons are preserved; their older Node 20 examples are not reused here.

The Python constraints were resolved with pip for the existing three direct requirements. Linux's `greenlet` version was verified against PyPI. Both functional workflows use the same constraint block. It is an updateable version snapshot, not a full hash lock. [Take-home maintenance](take-home/3-maintain-dependencies.md) explains direct pins and snapshot refresh.

## Verified action pins

These release tags resolved to the following commit objects through the owners' GitHub API on 2026-09-22 UTC. Their `action.yml` files declare Node 24. Full commit pins are used in all starter workflows.

| Action release | Verified commit |
|---|---|
| [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| [actions/setup-node v7.0.0](https://github.com/actions/setup-node/releases/tag/v7.0.0) | `820762786026740c76f36085b0efc47a31fe5020` |
| [actions/setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0) | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| [actions/dependency-review-action v5.0.0](https://github.com/actions/dependency-review-action/releases/tag/v5.0.0) | `a1d282b36b6f3519aa1f3fc636f609c47dddb294` |
| [actions/upload-artifact v7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1) | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |

Maintainers can resolve a candidate tag with `gh api repos/OWNER/ACTION/git/ref/tags/TAG`. If it references an annotated tag object, resolve that object's commit too. Read the release notes and action inputs before updating. A pin provides immutability, not a guarantee that the action is safe.

## Exercise sources

| Exercise | Primary evidence |
|---|---|
| Code | [CodeQL `py/flask-debug`](https://codeql.github.com/codeql-query-help/python/py-flask-debug/): security severity 7.5, included in the default Python suite |
| Dependency before | [GHSA-ffqj-6fqr-9h24](https://github.com/advisories/GHSA-ffqj-6fqr-9h24): high, PyJWT `>=1.5.0,<2.4.0` |
| Later PyJWT advisory | [GHSA-752w-5fwx-jx9f](https://github.com/advisories/GHSA-752w-5fwx-jx9f): high, `<=2.11.0`, first patch 2.12.0 |
| Dependency after | [PyPI PyJWT 2.14.0](https://pypi.org/project/PyJWT/2.14.0/); GitHub Advisory API lookup for `PyJWT@2.14.0` returned an empty list on 2026-09-22 |
| Secret fixture | Official [GitHub Skills step at 77045e0](https://github.com/skills/introduction-to-secret-scanning/blob/77045e069f9deda2beba27990d65899c4ee4b221/.github/steps/3-enable-push-protection.md) explicitly labels its training value inactive |
| Push repair | [CLI repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line) and [web repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-in-the-github-ui) |
| Environment | [Deployment protections](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) and [environment REST API](https://docs.github.com/en/rest/deployments/environments) |

The candidate PyJWT 2.10.1 was rejected during authoring because the advisory API reported a later high-severity issue. Recheck the shipped repair before each event. An advisory lookup does not prove GitHub discovered the exercise manifest; actual workflow evidence is recorded separately.

Do not infer a safe secret fixture from search-result prose. This kit uses only the attributed, delimiter-masked GitHub Skills value and never authenticates with it. The course's bypass activity and initial disable-protection activity are deliberately excluded. See [fixture provenance and route status](fixtures/secret-validation.md).

## Attribution

Pets source remains under its [original license](SOURCE-LICENSE). The reused inactive fixture is covered by [GitHub Skills' license](fixtures/SKILLS-LICENSE). Other lesson text is written for this workshop; linked documentation is not copied into the package.

## Checkpoint

Before changing a pin or fixture, update the evidence, rerun local and authorized live checks, and issue a new kit version. Do not retag an existing release or claim a source lookup is an executed control.
