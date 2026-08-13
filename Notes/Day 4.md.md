# Day 4 — Structured Outputs

**Objective:** Make AI produce predictable outputs.

---

## 📖 Theory

### The problem this solves

So far, `ask()` returns free-form text — a paragraph, a sentence, whatever the model felt like writing. That's fine for a chat app, but useless if another program needs to *read* the AI's answer automatically. Imagine you want to save "title, summary, keywords" into a database — you can't reliably `.split()` a paragraph to find those three things. You need the AI to respond in a **fixed, predictable shape** every time. That's what "structured output" means.

### JSON

**JSON (JavaScript Object Notation)** is a text format for representing structured data as key-value pairs — the universal language computers use to pass structured data around.

```json
{
  "title": "Understanding APIs",
  "summary": "APIs let programs talk to each other over the internet.",
  "keywords": ["API", "client", "server"]
}
```

Instead of asking the AI "explain APIs" and getting back a paragraph, Day 4 asks it to fill in *exactly* this shape — every time, no exceptions.

### Structured Output (the technique)

Modern LLM APIs let you tell the model "your response must match this exact shape," and the API enforces it — the model literally cannot return malformed JSON when this mode is on. This is different from just *asking nicely* in the prompt ("please respond in JSON") — that can still fail. True structured output mode is enforced by the API itself.

### Pydantic (basic idea)

**Pydantic** is a Python library for defining "what a valid piece of data looks like," then automatically checking real data against that definition.

```python
from pydantic import BaseModel

class ArticleSummary(BaseModel):
    title: str
    summary: str
    keywords: list[str]
```

This says: "A valid `ArticleSummary` *must* have a `title` (text), a `summary` (text), and `keywords` (a list of text items)." If the AI's response is missing a field, or has the wrong type, Pydantic raises a clear error immediately — instead of your program crashing confusingly three steps later.

### Parsing

**Parsing** just means: taking raw text (or JSON) and converting it into a Python object you can actually use — e.g. turning the JSON string above into a Python dictionary (or a Pydantic object) so you can write `result.title` instead of manually searching through text for it.

---

## 🎥 Best Resource

Official OpenAI *Structured Outputs* documentation (or the equivalent docs page for whichever provider you're using — Groq follows the same OpenAI-compatible format)

## 📚 Reading

JSON basics — any short "JSON in 5 minutes" style article/video works

---

## 💻 Coding Exercise

Extend `ask_structured()` in `src/assistant.py` so that, given a block of text, it returns a dictionary with exactly three keys: `title`, `summary`, `keywords`.

**The simplest working approach** (good enough for Day 4 — doesn't require a fancy structured-output API feature): tell the model very explicitly in the system prompt to return *only* valid JSON in that exact shape, then parse the response with Python's built-in `json` module.

---

## 🛠️ Today's Feature

The assistant can return structured data — given any text, it returns `{"title": ..., "summary": ..., "keywords": [...]}` instead of a free-form paragraph.

---

## 🧠 Quiz

1. Why is free-form text output not good enough when another program needs to read the AI's answer?
2. What's the difference between *asking* the model nicely for JSON in the prompt, vs. using an enforced structured-output mode?
3. What does a Pydantic model actually check for you?
4. What does "parsing" mean, in one sentence?
5. In the `ArticleSummary` example, what type is `keywords`, and why is that a good type for it?

## ⭐ Bonus

Add validation: after getting the AI's JSON response, check that all three fields are present and non-empty *before* trusting the result — print a clear error if something's missing instead of silently continuing with broken data.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| `json.decoder.JSONDecodeError` | The model added extra text before/after the JSON (e.g. "Sure! Here's your JSON:") | Be very explicit in the system prompt: "Respond with ONLY valid JSON, no other text" |
| `KeyError: 'keywords'` | The model's JSON didn't include one of your expected fields | Add a Pydantic model (or manual check) to validate the shape before using it |
| Keywords come back as one long string instead of a list | Prompt wasn't specific about the *type* you want for that field | Explicitly say "keywords as a JSON array of strings" in the prompt |

## ✅ Checklist

- [ ] `ask_structured()` reliably returns a dict with `title`, `summary`, `keywords`
- [ ] Tested on a few different input texts
- [ ] Validation added (bonus) — missing fields are caught, not silently ignored
- [ ] Git commit made
