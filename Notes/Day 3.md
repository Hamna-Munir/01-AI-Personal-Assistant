# Day 3 — Prompt Engineering

**Objective:** Control AI responses.

---

## 📖 Theory

### System Prompt

The **system prompt** is an instruction that sets the AI's role and behavior *before* the conversation starts. The user never sees it, but it shapes everything the model does. It's the closest thing to "configuring" an LLM without retraining it.

```python
MODES = {
    "general": "You are a helpful, concise assistant.",
    "grammar": "You correct grammar and spelling only. Do not change meaning or tone.",
}
```

Same underlying model, completely different behavior — just by changing this one string. This is the core idea behind today's feature (multiple assistant "modes").

### User Prompt

The **user prompt** is the actual question or request — what your user types in. It's the "content" the system prompt tells the model how to handle.

```python
messages = [
    {"role": "system", "content": "You correct grammar only."},
    {"role": "user", "content": "he dont know nothing about it"},
]
```

### Assistant Prompt

In a multi-turn conversation, the **assistant's own previous replies** get fed back in as `{"role": "assistant", "content": "..."}` messages. This is what lets the model "remember" what it already said — you'll wire this up for real on Day 5, but it's worth knowing the role exists from today.

### Temperature

**Temperature** controls how random vs. predictable the output is, on a scale roughly from 0 to 2:

- **Low (0–0.3):** focused, deterministic, same-ish answer every time. Good for factual tasks, grammar correction, structured output.
- **Medium (0.5–0.8):** balanced — the default sweet spot for general chat.
- **High (1.0+):** more creative, more varied, more likely to go off in unexpected directions. Good for brainstorming, creative writing.

There's no universally "correct" temperature — it depends on the task. Grammar Fix mode should probably use a *low* temperature (you don't want creative liberties with someone's sentence); a "brainstorm story ideas" mode should use a *higher* one.

### Tokens

LLMs don't process text character-by-character or even word-by-word — they process **tokens**, which are chunks of text (often close to, but not exactly, whole words — e.g. "unbelievable" might split into "un" + "believable"). Every API call has:

- **Input tokens** — your prompt + system prompt + conversation history
- **Output tokens** — the AI's reply

Both cost money and count toward the model's **context window** (the maximum tokens it can "see" at once). This is why conversation memory (Day 5) can't just grow forever — eventually you'd exceed the context window.

### Prompt Design

A few practical principles that consistently improve results:

1. **Be specific.** "Summarize this" is weaker than "Summarize this in 3 bullet points, focused on action items."
2. **Give the format you want.** If you want JSON, say so explicitly (this is the whole topic of Day 4).
3. **Show, don't just tell, when possible.** One example of the output style you want ("few-shot prompting") often works better than a paragraph describing it.
4. **Keep system and user prompts from contradicting each other.** If the system prompt says "always respond in French" and the user prompt says "respond only in English," the model has to guess which instruction wins — avoid putting yourself in that position.

---

## 🎥 Best Resource

DeepLearning.AI – *Prompt Engineering* (pick a beginner-level lesson from their short courses)

## 📚 Reading

[Prompt Engineering Guide](https://www.promptingguide.ai/) — read the "Basics" and "Techniques" sections

---

## 💻 Coding Exercise

Test the same user question across 5 different prompt styles/system prompts and compare the outputs — this builds intuition for how much the system prompt actually matters. For example, ask "Explain recursion" with:
1. No system prompt at all
2. `"You are a helpful assistant."`
3. `"Explain like I'm five years old."`
4. `"You are a strict computer science professor. Be technically precise."`
5. `"Explain in exactly two sentences."`

---

## 🛠️ Today's Feature

The assistant now has multiple modes, each with its own system prompt (already scaffolded in `src/assistant.py`'s `MODES` dict):

- **General Chat** — open-ended conversation
- **Grammar Fix** — corrects grammar/spelling only, preserves meaning
- **Explain** — explains a concept simply, beginner-friendly
- **Summarize** — condenses text into bullet points

---

## 🧠 Quiz

1. What's the difference between a system prompt and a user prompt?
2. Why would Grammar Fix mode use a *lower* temperature than a creative-writing mode?
3. What's a token, roughly, and why does it matter for cost and context window?
4. Give one concrete example of making a vague prompt more specific.
5. What happens if the system prompt and user prompt give conflicting instructions?

## ⭐ Bonus

Create your own custom system prompt for a 5th mode — for example, "Interview Prep" (asks you a mock interview question and gives feedback on your answer), or "Roman Urdu Translator."

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Vague, generic responses | System prompt too broad, or missing entirely | Be specific about role, tone, and constraints in the system prompt |
| Model ignores part of your instructions | Conflicting instructions between system and user prompts | Make sure both prompts agree; put the most important constraint last in the user prompt as a reminder |
| Wildly inconsistent answers to the same question | Temperature set too high for a factual/deterministic task | Lower the temperature (try 0.2–0.3) for tasks that need consistency |

## ✅ Checklist

- [ ] All 4 modes implemented and behave noticeably differently from each other
- [ ] Tested the same question across different system prompts
- [ ] Custom system prompt (bonus) created
- [ ] Git commit made
