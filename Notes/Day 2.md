# Day 2 — Python for AI Projects

**Objective:** Learn only the Python needed for AI engineering.

---

## 📖 Theory

### Functions

A function is a named, reusable block of code. Instead of copy-pasting the same logic everywhere, you write it once and call it by name.

```python
def ask(prompt: str, mode: str = "general") -> str:
    ...
    return reply
```

Why this matters for AI projects specifically: every "feature" you build this week (asking a question, checking grammar, remembering conversation) is going to be its own function. Clean functions are what let you *add* a feature on Day 5 without breaking what you built on Day 1.

A good function does **one thing**. If you find yourself writing "and" when describing what a function does ("it sends the prompt *and* saves it to a file *and* formats the output"), it's probably three functions wearing a trench coat.

### Modules

A **module** is just a Python file (`.py`) that you can import from. `config.py` is a module. `assistant.py` is a module. Splitting code into modules is how a 300-line single file becomes 4 focused, readable files.

```python
# src/config.py
OPENAI_API_KEY = "..."
```

```python
# src/assistant.py
from src.config import OPENAI_API_KEY
```

### Imports

`import` is how one module uses code defined in another. There are two common styles:

```python
import src.config                      # access as src.config.OPENAI_API_KEY
from src.config import OPENAI_API_KEY  # access directly as OPENAI_API_KEY
```

Use `from X import Y` when you only need one or two specific things from a module — it keeps your code shorter and clearer about exactly what you're using.

**Circular imports** (a common Day 2 bug): this happens when `a.py` imports from `b.py`, and `b.py` also imports from `a.py`. Python can't resolve which one should load first, and you get an `ImportError`. Fix: restructure so shared code lives in a third module both can import from (this project uses `config.py` for exactly this reason — both `assistant.py` and `main.py` import *from* it, but it doesn't import from either of them).

### Classes (basic)

A class bundles related data and behavior together. You don't need deep OOP theory for this week — just the basic shape:

```python
class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.history = []          # data the object holds

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})   # behavior
```

`__init__` runs when you create the object (`ConversationMemory()`), and sets up its starting state. `self` refers to "this particular instance" — it's how the object keeps track of its own data separately from any other instance. You'll build exactly this class for real on Day 5.

### File organization

By the end of today, the project should look like this (already scaffolded in this repo):

```
01-AI-Personal-Assistant/
├── main.py           # entry point — what you actually run
├── src/
│   ├── config.py       # settings & API key loading
│   ├── assistant.py    # core AI logic
│   └── memory.py       # conversation memory (Day 5)
```

The guiding principle: **`main.py` should be short.** It orchestrates; it shouldn't contain the actual logic. If `main.py` is 200 lines long, logic that belongs in `src/` has leaked into the entry point.

---

## 🎥 Best Resource

Corey Schafer – *Python Modules & Imports* (YouTube)

## 📚 Reading

[Python documentation — Modules](https://docs.python.org/3/tutorial/modules.html)

---

## 💻 Coding Exercise

Split your Day 1 code into three files (already stubbed in this repo):

- `main.py` — entry point, keeps the `while` loop for chatting
- `src/assistant.py` — the `ask()` function and mode logic
- `src/config.py` — API key and settings loading

Run it the same way as Day 1:
```bash
python main.py
```
It should behave identically to Day 1 — the point of refactoring is that *behavior doesn't change*, only the organization does.

---

## 🛠️ Today's Feature

The assistant works using modular code — same functionality as Day 1, but split across purpose-built files instead of one script.

---

## 🧠 Quiz

1. What's the difference between a function and a module?
2. Why does `main.py` import from `src/assistant.py` instead of the other way around?
3. What causes a circular import, and how do you avoid one?
4. What does `self` refer to inside a class method?
5. Why split one working file into three, if the behavior doesn't change?

## ⭐ Bonus

Write one small helper function of your own — for example, a `format_reply(text: str) -> str` that trims whitespace and capitalizes the first letter of the AI's response before printing it.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| `ImportError: cannot import name X` | Circular import between two modules | Move shared code into a third module neither depends on |
| `ModuleNotFoundError: No module named 'src'` | Running from the wrong folder, or missing `__init__.py` | Run commands from the project root; confirm `src/__init__.py` exists |
| Works in one file, breaks after splitting | A function used a variable defined elsewhere in the same file, not realized until split | Explicitly import or pass in everything a function needs — don't rely on "it happened to be in scope" |

## ✅ Checklist

- [ ] `main.py`, `src/assistant.py`, `src/config.py` each have a clear, single responsibility
- [ ] App still runs and behaves exactly like Day 1
- [ ] No circular imports
- [ ] Git commit made
