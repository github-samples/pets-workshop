# Demo setup

This repository is a **training sandbox** for a GitHub Copilot course. It deliberately
contains bugs, an insecure endpoint, synthetic personal data and a failing CI pipeline.
None of it is production code.

## Demo asset map

| Demo asset | Lives in | Training module it supports |
| --- | --- | --- |
| Clean codebase for `@workspace` / `#codebase` (tutorial text removed) | `content/` deleted | Context & the `#codebase` / `@workspace` tools |
| Absent `.github/copilot-instructions.md` (written live) | — (intentionally missing) | Authoring custom instructions |
| Leftover instruction files removed | `.github/instructions/` deleted | Customization / instructions hygiene |
| Concise onboarding README | [README.md](README.md) | Explaining / summarising a repo |
| Legacy firmware to comprehend | [app/firmware/kennel_door_controller.c](app/firmware/kennel_door_controller.c), [app/firmware/kennel_door_controller.h](app/firmware/kennel_door_controller.h) | Explaining unfamiliar / legacy code |
| Notebook with committed synthetic-PII output | [notebooks/shelter_intake_analysis.ipynb](notebooks/shelter_intake_analysis.ipynb) | Privacy / data-leak review; notebook debugging (orphaned + unexplained cells) |
| Insecure request handler (SQL injection, raw error) | [app/server/app.py](app/server/app.py) — `search_dogs` | Security review / vulnerability spotting |
| Four failing unit tests (four distinct bugs) | [app/server/test_app.py](app/server/test_app.py) | Debugging & fixing failing tests |
| Failing CI pipeline (tests + lint) | [.github/workflows/ci.yml](.github/workflows/ci.yml) | Debugging a pipeline failure from the terminal |
| Between-session reset tooling | [scripts/reset-demo.sh](scripts/reset-demo.sh), [scripts/README.md](scripts/README.md) | Facilitator workflow |

### The four planted test failures

Run `python -m pytest app/server/test_app.py`. Exactly four tests fail, each for a
different reason:

| Test | Failure | Cause |
| --- | --- | --- |
| `test_get_dogs_default_per_page` | `AssertionError: 6 != 10` | Asserts a value the code genuinely returns differently |
| `test_get_dog_breed_field` | `KeyError: 'breed_name'` | Wrong key name in the response dict |
| `test_search_dogs_result_shape` | `AttributeError: '_decode_rows'` | Calls a helper that does not exist |
| `test_search_cached_result` | `TypeError: 'NoneType'` | Depends on another test's state, so fails in isolation |

## Commands

### Before a session

```bash
# Backend
cd app/server
pip install -r requirements.txt
python utils/seed_database.py
python app.py                     # http://localhost:5100

# Frontend (separate terminal)
cd app/client
npm install
npm run dev                       # http://localhost:4321

# Server tests (should report exactly 4 failures)
python -m pytest app/server/test_app.py
```

### Tag the baseline (once)

```bash
git add -A
git commit -m "Prepare training demo baseline"
git tag demo-baseline
```

### Reset after a session

```bash
bash scripts/reset-demo.sh
```

The reset discards working-tree changes, removes untracked files, deletes any
live-authored `.github/copilot-instructions.md`, and hard-resets to `demo-baseline`.
It refuses to run on `main` when `origin` is the canonical upstream
(`github-samples/pets-workshop`).

## Notes and limitations

- **Astro build not verified here** — Node.js/npm is not installed in the setup
  environment. No client files were changed, so the build is unaffected, but run
  `npm install && npm run build` in `app/client` once to confirm on your machine.
- **Notebook output is hand-authored, not executed** — `pandas` is not an allowed
  dependency, so the committed output (including the synthetic adopter table with
  fictional `Musterstraße` / `Example Road` addresses, postcodes and phone numbers)
  was written directly into the `.ipynb` rather than produced by a kernel run. It is
  visible without running the notebook. Do not "Restart & Run All" in front of the
  audience — the code cells import `pandas` and reference an undefined variable, which
  would clear the committed output.
- **`demo-baseline` tag is not created automatically** — create it once (above) before
  the first reset, or `scripts/reset-demo.sh` will refuse to run.
- **A local `.venv/` was created** at the repo root to run the tests; it is gitignored.
