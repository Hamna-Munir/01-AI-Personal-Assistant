# Day 6 — Clean Code & Refactoring

**Objective:** Turn beginner code into professional code.

---

## 📖 Theory

### Why this day exists

By Day 5, your project works — but "works" and "professional" aren't the same thing. Day 6 isn't about adding a new feature; it's about making the *existing* code easier to read, easier to debug, and easier for someone else (or future-you, in 3 months) to understand at a glance. This is the difference between a script that happens to run, and a project someone would trust in production.

### Clean Functions

A clean function has three properties:

1. **It does one thing.** `ask()` sends a prompt and returns a reply — it doesn't *also* print things, *also* save to a file, and *also* validate input. If a function's name needs the word "and" to describe it, split it.
2. **It's short enough to read in one glance.** If you have to scroll to see the whole function, it's probably doing too much.
3. **Its name tells you what it does without reading the body.** `format_reply()` is clean. `process()` is not — process *what*, exactly?

### Naming

Good names remove the need for comments. Compare:

```python
# bad
x = get(u)
if x > 20:
    do(x)

# clean
user_age = get_user_age(user_id)
if user_age > MINIMUM_AGE:
    grant_access(user_age)
```

The second version needs zero comments to understand — the names carry the meaning.

### Comments

Comments should explain **why**, not **what**. Code already says *what* it does (if it's clean); comments are for context code can't express on its own:

```python
# bad — just restates the code
temperature = 0.3  # set temperature to 0.3

# good — explains a non-obvious reason
temperature = 0.3  # low temperature: we want consistent, predictable JSON output
```

You've actually already seen this pattern — look back at the comment on `temperature=0.3` in `ask_structured()` from Day 4.

### Error Handling

Right now, if the API key is missing, or the network fails, or the model returns garbage, your program likely crashes with a raw Python traceback — confusing for anyone using the app. Clean error handling means catching the *specific* problems you can anticipate and giving a clear, human-readable message instead:

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Sorry, something went wrong talking to the AI: {e}")
    return None
```

The goal isn't to hide every error silently — it's to fail *clearly* instead of *confusingly*.

### Logging (basic)

`print()` statements are fine for a quick script, but they can't be turned off, categorized, or saved to a file later. Python's built-in `logging` module solves this:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Sending request to model %s", MODEL_NAME)
logger.warning("Response took longer than expected")
logger.error("API call failed: %s", str(e))
```

You don't need anything fancy this week — just replacing a couple of your `print()` debug statements with `logger.info()` is enough to get the idea.

---

## 🎥 Best Resource

Any beginner-friendly summary of "Clean Code" principles (Robert C. Martin's *Clean Code* is the classic reference — you don't need to read the whole book, just the core ideas around functions and naming)

## 📚 Reading

[PEP 8](https://peps.python.org/pep-0008/) — Python's official style guide. Skim the sections on naming conventions and whitespace; you don't need to memorize it, just recognize the patterns.

---

## 💻 Coding Exercise

Go back through every file in `src/` and `main.py` and refactor with today's lens:

1. Any function doing more than one thing? Split it.
2. Any unclear variable/function names? Rename them.
3. Any comment that just repeats the code next to it? Delete it. Any place that *needs* a "why" comment and doesn't have one? Add it.
4. Wrap at least one risky operation (the actual API call is the best candidate) in a `try/except` with a clear error message.
5. Add basic logging for at least one meaningful event (e.g. "sending request," "received response").

---

## 🛠️ Today's Feature

No new user-facing feature today — the deliverable is a **professional-looking, readable codebase** that does exactly what it did yesterday, just cleaner.

---

## 🧠 Quiz

1. What are the three properties of a "clean" function?
2. What should a comment explain that the code itself can't?
3. What's the difference between failing "clearly" and failing "confusingly"?
4. Why is `logging` generally preferred over scattered `print()` statements in a real project?
5. Look at your own `ask()` function — is there anything in it right now that violates the "does one thing" rule?

## ⭐ Bonus

Add logging around your `ask()` and `ask_structured()` calls — log when a request starts, and log an error if it fails, instead of letting a raw traceback show.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Refactoring broke something that worked yesterday | Changed logic while renaming, not just names | Refactor in small steps — rename *only*, test, then restructure *only*, test again. Don't do both at once. |
| `try/except` swallows errors silently, bugs get harder to find | Caught `Exception` broadly and didn't print/log anything | Always print or log the actual error message inside the `except` block — never a bare `except: pass` |
| Logging shows nothing in the terminal | Forgot to call `logging.basicConfig(level=logging.INFO)` before logging | That line must run once, early, before any `logger.info(...)` calls |

## ✅ Checklist

- [ ] Every function does one clear thing
- [ ] Names are self-explanatory without needing comments to clarify them
- [ ] At least the main API call is wrapped in error handling with a clear message
- [ ] Basic logging added for at least one key event
- [ ] App still behaves identically to before refactoring
- [ ] Git commit made
