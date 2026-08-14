# Day 5 — Conversation Memory

**Objective:** Remember previous messages.

---

## 📖 Theory

### The problem this solves

Right now, every time you call `ask()`, the model has **zero idea** what you said a moment ago. Try this with your current app: say "My name is Hamna," then ask "What's my name?" — the AI will have no clue. Each call to the API is completely independent; the model doesn't automatically remember anything between calls. Memory has to be built by *you*, on the client side.

### Context Window

The **context window** is the maximum amount of text (measured in tokens — remember Day 3) a model can "see" at once, covering the system prompt + all conversation history + the new message, combined. Different models have different limits (e.g. some see the last 8,000 tokens, others see 128,000+).

This is *why* memory can't just grow forever — eventually the conversation history plus your new question would exceed the context window, and older messages have to be dropped (or summarized) to make room.

### Chat History

The trick to "memory" is almost embarrassingly simple: **you just re-send the entire conversation every single time.** The model isn't remembering anything internally between calls — *you* are keeping a list of everything said so far, and sending that whole list along with every new message.

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Hamna."},
    {"role": "assistant", "content": "Nice to meet you, Hamna!"},
    {"role": "user", "content": "What's my name?"},   # <- new message
]
```

Sent together like this, the model can see the earlier turns in the same request and correctly answer "Your name is Hamna." From the model's perspective, it's not "remembering" across time — it's reading a longer document that happens to contain the whole conversation so far.

### Memory Basics

Practically, "memory" in a simple assistant like this one is just:
1. A list that stores every `{"role": ..., "content": ...}` turn (this is exactly what `src/memory.py`'s `ConversationMemory` class already does — built back on Day 2)
2. Every time you call the model, you send the *whole list* instead of just the newest message
3. After the model replies, you append its reply to the list too, so the next call includes it

---

## 🎥 Best Resource

Look at your own LLM provider's official docs page on multi-turn conversations / chat history — the concept is identical across OpenAI, Groq, and most others since they share the same `messages` format.

## 📚 Reading

Any short guide/example showing a multi-turn `messages` array (see the code block above — that's really the whole idea).

---

## 💻 Coding Exercise

Wire `ConversationMemory` (already built in `src/memory.py`) into `ask()`:

1. In `main.py`, every time the user sends a message, call `memory.add("user", user_input)` *before* calling the API
2. Change `ask()` in `src/assistant.py` to accept the memory's message list instead of building a fresh 2-message list every time
3. After getting the reply, call `memory.add("assistant", reply)` so it's included in the *next* call too

---

## 🛠️ Today's Feature

The assistant remembers the conversation — you can say "My name is Hamna" in one turn, and ask "What's my name?" two turns later, and it will answer correctly.

---

## 🧠 Quiz

1. Does the AI model itself remember anything between separate API calls?
2. What is a context window, in your own words?
3. Why can't conversation history just grow forever?
4. What three roles appear in a `messages` list, and what does each one represent?
5. What two things does `main.py` need to do, each turn, to keep memory working correctly?

## ⭐ Bonus

Add a `clear` command (already stubbed in `main.py`!) that resets `ConversationMemory` — confirm it actually works: have a conversation, run `clear`, then ask "What's my name?" again — it should no longer know.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| AI still doesn't remember earlier turns | Forgot to call `memory.add()` for either the user message or the assistant's reply | Make sure *both* sides of every turn get added to memory, not just the user's messages |
| Responses get slower / errors about context length | Memory grown too large, exceeding the model's context window | `ConversationMemory` already truncates to `max_turns` — lower that number if needed |
| `clear` command doesn't seem to work | Memory object recreated on every loop iteration instead of once outside the loop | Make sure `memory = ConversationMemory()` is created *once*, before the `while True:` loop, not inside it |

## ✅ Checklist

- [ ] Assistant correctly recalls information from earlier in the same session
- [ ] `clear` command tested and confirmed working
- [ ] Memory doesn't grow unbounded (truncation confirmed in `memory.py`)
- [ ] Git commit made
