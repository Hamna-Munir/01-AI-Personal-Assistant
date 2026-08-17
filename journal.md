# 📓 Engineering Journal — Week 1

**Project:** `01-AI-Personal-Assistant`
**Week Theme:** Talking to AI

This journal is a running log across Day 1 → Day 7. Each entry answers the
same four questions: what happened, what problems came up, how I thought
through them, and what I actually learned. Fill in one section right after
that day's work, while it's still fresh — not at the end of the week from
memory.

---

## Day 1 — AI Fundamentals & Environment Setup

**Date:** 10 August 2026

**What I worked on today**
- Read through AI vs ML vs Deep Learning, what an LLM actually is, and how it's different from a database that "knows" facts
- Set up the project folder, created and activated a virtual environment
- Installed `openai` and `python-dotenv`
- Created `.env` from `.env.example` and added my real API key
- Filled in the `TODO(Day 1)` sections in `src/assistant.py` and ran `main.py` to get my first AI response

**Problems I ran into**
- First run threw an `Invalid API key` error even though I was sure I'd copied it correctly
- `.env` wasn't loading at all on a second attempt — the script couldn't see the key even though the file existed

**How I thought through it**
- For the invalid key: re-opened the dashboard and re-copied it character by character — turned out I'd grabbed a trailing space along with the key when copying
- For the `.env` not loading: checked where the script was actually being run from vs where `.env` lived — the file was one folder up from the project root, not inside it. Moved it into the root next to `main.py` and `load_dotenv()` picked it up immediately

**Progress**
- [x] Environment ready (venv created & activated)
- [x] SDK installed
- [x] `.env` created with a real API key
- [x] First API response received and printed
- [x] Git commit made

**Reflection — in my own words, what's the actual difference between the API and ChatGPT?**
- ChatGPT is the finished restaurant meal — a full product with a chat UI, memory, and safety layers already built in. The API is just the raw ingredients: I send text, I get text back, and everything else (the interface, how history is stored, how errors are shown) is on me to build. Today I was working directly with the ingredients for the first time instead of just eating the meal.

---

## Day 2 — Python for AI Projects

**Date:** 11 August 2026

**What I worked on today**
- Went through functions, modules, imports, basic classes, and file organization
- Split yesterday's single-file script into `main.py`, `assistant.py`, and `config.py`
- Moved the API-calling logic into `assistant.py` and kept `main.py` as just the entry point

**Problems I ran into**
- Didn't personally hit a real blocker today — the split went smoothly once I understood the pattern
- Common problem others tend to hit here: circular imports (e.g. `assistant.py` importing from `main.py` while `main.py` imports from `assistant.py`), and imports breaking because the script is run from a different folder than expected
- Solution for both: keep a one-directional dependency flow (`main.py` → `assistant.py` → `config.py`, never the reverse), and always run scripts from the project root so relative imports resolve consistently

**How I thought through it**
- Before splitting, mapped out on paper which piece needed which — config values needed by assistant, assistant logic needed by main — so the import direction only ever went one way

**Progress**
- [x] Code split into `main.py`, `assistant.py`, `config.py`
- [x] Assistant still works after the split
- [x] No circular imports or broken paths

**Reflection — why did splitting one file into three actually make the project easier to work with (or did it)?**
- It made it obvious where to look for something — config values in one place, API logic in another, entry point separate from both. Even though the app does the exact same thing as yesterday, I can now change how the assistant talks to the API without touching how the program starts.

---

## Day 3 — Prompt Engineering

**Date:** 12 August 2026

**What I worked on today**
- Learned the difference between system, user, and assistant prompts, plus temperature and tokens
- Took 5 vague prompts and rewrote them to be specific about audience, format, and goal
- Built out the assistant's modes: General Chat, Grammar Fix, Explain, Summarize

**Problems I ran into**
- Nothing major personally — the "vague vs specific" idea clicked fast once I saw the before/after examples
- Common problem here: writing a prompt that's clear to a human but still ambiguous to the model (e.g. "make it better" with no definition of "better"), or stacking conflicting instructions in the same prompt (e.g. "be concise" and "explain in detail" at once)
- Solution: be explicit about format, length, and audience every time, and if two instructions could conflict, decide which one wins and say so directly in the prompt

**How I thought through it**
- Tested each mode's prompt against the same input a few times to see if the output stayed consistent — inconsistent output was usually a sign the instruction was still too loose

**Progress**
- [x] Tested 5 different prompt styles
- [x] Modes working: General Chat, Grammar Fix, Explain, Summarize
- [x] Wrote my own system prompt

**Reflection — what changed in the assistant's output when I gave it a real system prompt vs none at all?**
- Without a system prompt, the model would answer reasonably but inconsistently — sometimes formal, sometimes casual, sometimes adding unnecessary disclaimers. With a clear system prompt defining the role and constraints, the tone and format stayed consistent across different questions.

---

## Day 4 — Structured Outputs

**Date:** 13 August 2026

**What I worked on today**
- Learned what structured output means and got a basic feel for how Pydantic validates data
- Wrote a prompt that makes the model return JSON with `title`, `summary`, and `keywords`
- Parsed the JSON response and handled the case where the model wraps it in a code fence

**Problems I ran into**
- Didn't struggle much personally — got the JSON prompt right on close to the first try
- Common problem here: the model returning JSON wrapped in ```` ```json ```` fences even when told not to, or dropping a required field on some inputs
- Solution: strip code fences before parsing instead of assuming clean JSON, and validate the parsed result against a schema so a missing field fails loudly instead of causing a silent bug later in the UI

**How I thought through it**
- Ran the same prompt against a few very different inputs (a short sentence, a long paragraph, a list) to see if the JSON shape held up — it mostly did, except one edge case with very short input where "summary" came back nearly identical to the title

**Progress**
- [x] Assistant returns valid JSON (title / summary / keywords)
- [x] Output validated, not just trusted as-is
- [x] Handled a case where the model didn't return valid JSON

**Reflection — what's the actual risk of *not* validating a model's JSON output before using it?**
- If I just trust the raw text and pass it straight into the app, one malformed response (a missing field, broken JSON, an extra unexpected key) can crash the UI or silently display broken data. Validating means a bad response fails with a clear error I can catch, instead of quietly breaking something downstream.

---

## Day 5 — Conversation Memory

**Date:** 14 August 2026

**What I worked on today**
- Learned what a context window is and how chat history actually gets "remembered"
- Added storage for previous messages and included them in every new API call
- Added a command to clear the conversation and start fresh

**Problems I ran into**
- No real issues today — the concept that "memory" is just re-sending prior messages, not the model actually retaining anything, made everything click quickly
- Common problem here: history growing unbounded until it hits the model's token limit, or duplicate messages getting added when a function is called more than once
- Solution: cap or trim history to the most recent N turns, and make sure the "add message" function is only called exactly once per turn

**How I thought through it**
- Tested with a longer back-and-forth conversation to confirm the assistant actually referenced something said several turns earlier — it did, which confirmed the history was being passed correctly

**Progress**
- [x] Previous messages are stored and reused each turn
- [x] Conversation feels natural across multiple turns
- [x] Added a "clear memory" command

**Reflection — in my own words, what is a context window, and what happens if I ignore its limit?**
- The context window is the maximum amount of text (measured in tokens) the model can "see" at once — the system prompt, the full chat history, and the new message all count against it. If I ignore the limit and let history grow forever, eventually the request either gets rejected or the oldest, possibly important context silently gets cut off.

---

## Day 6 — Clean Code & Refactoring

**Date:** 15 August 2026

**What I worked on today**
- Reviewed clean function principles, naming conventions, and basic error handling/logging
- Refactored long functions in `assistant.py` into smaller, single-purpose ones
- Wrapped API calls in `try/except` and added basic logging instead of letting errors crash the app silently

**Problems I ran into**
- Nothing that blocked me — most of this was applying patterns I'd already been half-using
- Common problem here: functions that quietly do too many things at once (fetching, formatting, and printing all in one function), and duplicate logic copy-pasted across modes instead of shared in one place
- Solution: one function, one responsibility — split fetch/format/display apart — and pull any duplicated logic into a shared helper function

**How I thought through it**
- Went function by function and asked "what's the one thing this does?" — if the answer had an "and" in it, that was a signal to split it

**Progress**
- [x] Long functions broken into smaller ones
- [x] Consistent naming across the project
- [x] Error handling added around API calls
- [x] Basic logging added

**Reflection — what did the codebase look like before vs after refactoring, and what specifically got easier?**
- Before, most of the logic lived in one or two long functions that mixed API calls, formatting, and error handling together. After, each piece is separate and named for what it does, so tracing a bug now means looking at one small function instead of scrolling through a wall of code.

---

## Day 7 — Finalization & Deployment

**Date:** 16 August 2026

**What I worked on today**
- Wrote the README (features, setup steps, usage, project structure)
- Finalized `requirements.txt` and double-checked `.gitignore` excludes `.env` and `venv/`
- Pushed to GitHub and deployed on Streamlit Community Cloud, adding the API key as a platform Secret
- Tested the live deployed link in an incognito tab to confirm it matched local behavior

**Problems I ran into**
- Deployment itself went smoothly once I understood the platform's flow
- Common problem here: the app working locally but failing on deploy because a package used locally wasn't listed in `requirements.txt`, or the deployed app crashing with an auth error because the `.env` key was never added to the platform's Secrets (local `.env` files never get uploaded)
- Solution: regenerate `requirements.txt` with `pip freeze` from a clean venv right before pushing, and manually copy every key from `.env` into the platform's Secrets settings — they're two separate places that don't sync automatically

**How I thought through it**
- Treated "deployed" and "local" as two genuinely separate environments rather than assuming they'd behave the same — checked the live link fresh instead of assuming a successful local run meant deployment would just work

**Progress**
- [x] README complete
- [x] Screenshots added
- [x] `requirements.txt` finalized
- [x] `.env` confirmed excluded from git
- [x] Deployed and tested on a live link
- [x] `week-01-summary.md` written
- [x] GitHub updated

**Reflection — end of week: what's the difference between "runs on my machine" and "actually deployed," in practice?**
- "Runs on my machine" only proves the code works with my exact setup — my Python version, my installed packages, my local `.env`. "Actually deployed" means someone else, with none of that context, can open a link and have it work the same way. Getting there means making every dependency and every secret explicit instead of relying on things I happened to already have set up.

---

## 🔑 Week 1 — Biggest Lessons

1. An LLM doesn't "know" things the way a database does — it predicts likely text, which is why confident-sounding wrong answers ("hallucinations") happen.
2. Splitting code into focused files/functions isn't just tidiness — it directly made debugging and extending the assistant faster every single day after Day 2.
3. "Memory" and "structure" in an LLM app are illusions maintained by the code around the model (re-sending history, validating JSON) — the model itself doesn't retain or guarantee either on its own.
4. Deployment problems are almost never about the AI logic — they're about environment differences (missing dependencies, un-synced secrets) that only show up once the code leaves my machine.

## 🎯 Going into Week 2

Week 2 shifts from "getting an API call working" into **Prompt Engineering &
Reliable AI** — system instructions, templates, few-shot examples, and
evaluating prompts properly. Note here anything from this week that's
likely to matter there (e.g. where a vague prompt gave a weak result,
where a system prompt made a visible difference).

-
