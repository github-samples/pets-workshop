# GitHub Copilot: Cost-Aware Usage

Practical habits that reduce AI Credit consumption without reducing output quality.
Reference material for TKE Session 1, Modules 2 and 4.

---

## 0. The billing model changed

Since 1 June 2026, Copilot bills **GitHub AI Credits** based on token usage (input, output and cached tokens) instead of premium request units.

What that means in practice:

- Cost is now proportional to **context size**, not to the number of prompts.
- A single sloppy prompt with the whole repo attached can cost more than fifty tight ones.
- **Code completions and next edit suggestions are still free.** They do not consume credits.
- The old fallback to a cheaper model when you ran out is gone. Usage is governed by available credits and admin budget controls.

Everything below follows from that one fact: **context size is the invoice**.

---

## 1. Use the free surfaces first

These cost nothing:

| Surface | Use it for |
|---|---|
| Ghost text completions | Boilerplate, repetitive edits, the obvious next line |
| Next edit suggestions | Follow-on edits after a rename or signature change |
| Comment to code | Write the intent as a comment, let Copilot draft the body |

If completions can do the job, do not open chat. Most developers reach for chat far too early.

---

## 2. Scope the context deliberately

Cost, cheapest to most expensive:

```
implicit context  <  #selection  <  #file  <  #codebase
```

- **Implicit context is already free of charge to you in effort, not in tokens.** VS Code automatically attaches the active file, your current selection and the file name. You often do not need to attach anything at all.
- **`#selection`** is the narrowest explicit scope. Only appears in the picker when text is actually selected.
- **`#file`** when the answer depends on the file's structure, not one block.
- **`#codebase`** forces a semantic search across the project. Agents already run semantic search on their own when it makes sense, so typing it is usually redundant and always expensive.

> The habit to build: before you press enter, glance at what is attached. If you can see it in the request, you are paying for it.

Note: `#workspace` no longer exists. `#codebase` replaced it.

---

## 3. Shorter prompts, same result

- Slash commands are a few characters instead of a sentence. `/explain`, `/fix`, `/tests`, `/doc`.
- Repeated instructions belong in `copilot-instructions.md` or `AGENTS.md`, not retyped in every prompt.
- Reusable prompt files and agent skills turn a paragraph into `/my-command`.

---

## 4. Manage the conversation, not just the prompt

Long threads are expensive because the whole history is resent on every turn.

| Action | When |
|---|---|
| Watch the context meter in the chat input box | Always. Hover it for a token breakdown by category |
| `/compact` | The thread is long but you still need its conclusions |
| `/fork` | You want to explore an alternative without dragging the history along |
| New session (`/clear`) | New task. Do not reuse a thread out of laziness |

One thread per task. When the task is done, the thread is done.

---

## 5. Exclusions are a cost control

When an agent searches your workspace with grep or text search, **every match it gets back enters the context window**, including files it never opens.

Example: an agent greps for `calculateTotal`. Your repo has `node_modules/`, a `dist/` folder of minified bundles and a pile of build logs. The search returns 800 hits. The agent uses 3. You paid for all 800.

Exclusion settings stop those paths being searched at all, so the matches never exist.

| Setting | Hidden in Explorer | Excluded from search and grep | Excluded from semantic index |
|---|---|---|---|
| `.gitignore` | no | yes | yes |
| `files.exclude` | yes | yes | yes |
| `search.exclude` | no | yes | no |

`files.exclude` and `search.exclude` are VS Code settings, not files. Put them in `.vscode/settings.json` and commit that, so the whole team benefits:

```json
{
  "files.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true
  },
  "search.exclude": {
    "**/*.log": true,
    "**/coverage": true,
    "**/*.min.js": true
  }
}
```

Caveat: `.gitignore` is bypassed if you have the ignored file open or have text selected inside it.

---

## 6. A working index is cheaper than pasting

The semantic index lets Copilot retrieve the three relevant snippets instead of you pasting three whole files into chat. Cheaper and more accurate.

Index sources:

- **GitHub repositories.** GitHub builds and maintains it, usually available instantly. GitHub.com and Enterprise Cloud only, not Enterprise Server.
- **Azure DevOps repositories.** Built automatically once you sign in with your Microsoft account.
- **Everything else.** VS Code builds it locally. On for personal accounts, **off by default for organisations** unless an admin enables the policy.

Check the state in the Copilot status dashboard in the VS Code status bar. Force a rebuild with **Build Codebase semantic index** from the Command Palette.

If there is no index, agents still work. They fall back to grep, text search, file search and language intelligence. It is slower and less precise, not broken.

---

## 7. Match the model to the task

Do not default to the largest available model. Higher-capability models consume more credits per token. Reserve them for genuinely hard reasoning; use a smaller model for renames, docstrings, test scaffolding and formatting work.

---

## 8. Quality is a cost too

The cheapest request is the one you do not have to send twice.

- Precise input produces precise output. A vague comment produces a vague function.
- Read the inline diff before accepting. Reading it costs seconds; a bad merged suggestion costs a debugging session.
- Narrower context frequently produces a **better** answer, not just a cheaper one. Less noise for the model to weigh.

---

## Quick checklist

Before you press enter:

- [ ] Could a completion have done this instead of a chat request?
- [ ] Is the narrowest scope attached that could answer the question?
- [ ] Did I type `#codebase` out of habit?
- [ ] Is this the right thread, or should it be a new session?
- [ ] What does the context meter say?
- [ ] Does this repo have exclusions committed in `.vscode/settings.json`?

---

*Sources: VS Code AI features documentation and workspace context reference (September 2026), GitHub Copilot usage-based billing announcement (April 2026, effective 1 June 2026).*
