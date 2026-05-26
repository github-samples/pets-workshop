---
name: team-review-checklist
description: Team review rules applied automatically to every pull request — covers test coverage for new endpoints and Microsoft REST API error envelope compliance.
version: 0.1.0
scopes:
  - code-review
  - coding-agent
owners:
  - elbruno
  - april-yoho
---

# Team Review Checklist

This Skill encodes our team's standing review rules. When connected to Copilot
Code Review (or Copilot Coding Agent) at the repo level, Copilot applies these
rules automatically on every pull request — alongside its built-in analysis and
any other context sources (e.g. Microsoft Docs MCP).

Each rule below tells Copilot:

- **When** to flag (the condition).
- **What** to say in the review comment (the message).
- **Why** the rule exists (so Copilot can cite the reason in its comment).
- **Examples** of acceptable vs. unacceptable code where helpful.

---

## Rule 1 — New API endpoints must include a test file

**When to flag.** A pull request adds a new HTTP route, handler, or API
endpoint (Flask route, Express handler, FastAPI path operation, ASP.NET
controller action, Express Router, etc.) **and** the same pull request does
not add or modify a corresponding test under any of the project's recognized
test locations.

Recognized test locations include — but are not limited to:

- `tests/`
- `test/`
- `__tests__/`
- any file matching `*_test.*`, `*.test.*`, `*.spec.*`, or `test_*.*`

**What to say in the comment.**

> This pull request adds a new API endpoint but does not include a
> corresponding test. Per our team's review checklist, every new endpoint
> needs at least one test that exercises the happy path and the primary
> error path.

**Why.** Every new endpoint expands the public surface area of the service.
Tests are how we prevent regressions when other endpoints, models, or
shared middleware change later. This rule applies even for endpoints that
look trivial — small endpoints are exactly the ones that drift silently.

**What "good" looks like.** For a new `POST /api/pets/{id}/adopt`
endpoint on a Flask service, an acceptable companion test lives in
`tests/` (or `app/server/tests/`) and covers at minimum:

- A 200 path: adopt succeeds for an existing, non-adopted pet.
- A 404 path: adopting a non-existent pet returns the documented
  error response.

Posting a test alongside the route — even a small one — clears this rule.

---

## Rule 2 — Error responses must follow the Microsoft REST API error envelope

**When to flag.** A pull request adds or modifies an HTTP endpoint that
returns an error response (any non-2xx status code) **and** the body of
that error response does not follow the Microsoft REST API error envelope.

The envelope expected by this rule, per the Microsoft REST API guidelines,
is a JSON body of the shape:

```json
{
  "error": {
    "code": "string — a server-defined error code, e.g. PetNotFound",
    "message": "string — a human-readable message safe to display",
    "target": "string — optional, the field or resource the error refers to",
    "details": [
      {
        "code": "string",
        "message": "string",
        "target": "string"
      }
    ]
  }
}
```

At minimum, every error response must include an `error` object containing
both `code` and `message`. `target` and `details` are optional but
encouraged for validation errors.

**Examples of responses this rule flags.** Any of the following error
bodies are not compliant:

```python
# ❌ Plain string in a flat "error" field — no code, no envelope.
return jsonify({"error": "Pet not found"}), 404
```

```python
# ❌ Bare string body.
return "Pet not found", 404
```

```python
# ❌ Mixed shape — message at the top level, no error object.
return jsonify({"message": "Pet not found"}), 404
```

**Examples of responses this rule accepts.**

```python
# ✅ Microsoft REST API error envelope.
return jsonify({
    "error": {
        "code": "PetNotFound",
        "message": "Pet not found.",
        "target": "id"
    }
}), 404
```

**What to say in the comment.**

> This error response does not follow the Microsoft REST API error envelope.
> Error bodies on this service must include an `error` object containing
> at least `code` and `message`, and optionally `target` and `details`.
> Please update this response to match the envelope before merging.
>
> Reference: Microsoft REST API guidelines (via the Microsoft Docs MCP
> source connected to this repository).

**Why.** Consistent error shapes are how clients build robust error handling
without hand-coding per-endpoint quirks. Our service is consumed by both
internal and partner clients; deviating from the documented envelope makes
their integrations brittle and our error telemetry harder to aggregate.

---

## How this Skill produces clean review comments

When both rules above fire on the same pull request, each finding shows up
as a **separate** review comment so reviewers can resolve them
independently. The comment carries the **team-review-checklist** attribution
badge so it is clearly distinguishable from:

- Findings grounded in an external MCP context source (which carry that
  source's badge — e.g. **Microsoft Docs**), and
- Copilot's built-in analysis findings (which carry no badge).

This separation is intentional — it lets the team see at a glance which
parts of the review came from our standards vs. external guidance vs.
Copilot's baseline checks.

---

## Operational notes

- **Scope.** This Skill is scoped to both **Code Review** and **Coding
  Agent**, so the same rules apply whether a human opened the PR or
  Coding Agent did.
- **Trigger.** Re-runs automatically on every push to a PR branch and on
  PR open. No manual invocation required.
- **Cost.** Rules in this Skill are evaluated as part of the standard
  Copilot Code Review pass — they do not incur a separate billing line.
- **Updating the rules.** Edit this file on a branch, open a PR, and the
  updated rules take effect once that PR merges. There is no separate
  deployment step.
- **Disabling temporarily.** To pause this Skill without removing it,
  toggle its status to **Inactive** in repo Settings → Copilot →
  Code review → Custom checks.

---

## Out of scope for this Skill (intentionally)

To keep the Skill sharp and the review noise low, the following are
**not** enforced here — they are either covered elsewhere or are
intentionally left to Copilot's built-in analysis:

- General code style, naming, and formatting.
- Accessibility (handled by Copilot's built-in analysis).
- Security (handled separately by GitHub Advanced Security / CodeQL).
- Performance and complexity reviews.

If new rules are added later, keep each one narrow, name a single failure
mode, and include both a "flag when" condition and a "what to say"
message — same shape as the two rules above.
