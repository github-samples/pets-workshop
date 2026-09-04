# Demo Setup

This repository is a training sandbox for live GitHub Copilot demos. It deliberately contains synthetic data, planted test failures, an insecure endpoint, and a failing CI workflow.

## Demo asset map

| Demo asset | File | Training module |
| --- | --- | --- |
| Tutorial material removed for cleaner code search | deleted workshop tutorial directory | `@workspace` / `#codebase` context demos |
| Live-authored instructions start absent | `.github/copilot-instructions.md` intentionally missing | Custom instructions authoring |
| Unrelated instruction files removed | deleted files under `.github/instructions/` | Customization hygiene |
| Short repo overview | [README.md](README.md) | Repo summarization |
| Firmware-style code sample | [app/firmware/kennel_door_controller.c](app/firmware/kennel_door_controller.c), [app/firmware/kennel_door_controller.h](app/firmware/kennel_door_controller.h) | Legacy code comprehension |
| Notebook with committed synthetic contact data, an unexplained cell, and an orphaned cell | [notebooks/shelter_intake_analysis.ipynb](notebooks/shelter_intake_analysis.ipynb) | Notebook review and privacy demos |
| Insecure dog search endpoint | [app/server/app.py](app/server/app.py) | Security review |
| Four distinct test failures across nine tests | [app/server/test_app.py](app/server/test_app.py) | Debugging failing tests |
| CI workflow with test job and failing lint job | [.github/workflows/ci.yml](.github/workflows/ci.yml) | Pipeline debugging |
| Demo reset script and facilitator notes | [scripts/reset-demo.sh](scripts/reset-demo.sh), [scripts/README.md](scripts/README.md) | Session reset workflow |

## Commands to run before a session

```bash
python -m pip install -r app/server/requirements.txt pytest
python app/server/utils/seed_database.py
python app/server/app.py

cd app/client
npm install
npm run dev
```

Optional checks before the audience joins:

```bash
python -m pytest app/server/test_app.py
cd app/client && npm run test:e2e
```

## Commands to tag and reset the baseline

```bash
git add -A
git commit -m "Prepare training demo baseline"
git tag demo-baseline
```

```bash
bash scripts/reset-demo.sh
```

The reset script discards tracked changes, removes untracked files, deletes `.github/copilot-instructions.md` if it exists, and hard-resets to `demo-baseline`. It refuses to run on `main` when `origin` points at `github-samples/pets-workshop`.

## Incomplete items

- No repo task items remain incomplete.
- The Astro build command is included above, but it was not runnable in this environment because `npm` is not installed on PATH.
