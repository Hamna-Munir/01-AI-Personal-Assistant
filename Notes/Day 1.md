# Day 1 — AI Fundamentals & Environment Setup

**Objective:** Understand how an LLM works and make your first API call.

---

## 📖 Theory

### AI vs Machine Learning vs Deep Learning

These three terms get used interchangeably, but they're nested inside each other, like Russian dolls.

- **Artificial Intelligence (AI)** — the broadest term. Any technique that makes a machine act "smart" — even a simple set of `if/else` rules counts as AI (a chess program from the 1980s is AI).
- **Machine Learning (ML)** — a *subset* of AI where the system learns patterns from data instead of being explicitly programmed with rules. Example: a spam filter that learns from thousands of labeled emails what "spam" looks like.
- **Deep Learning (DL)** — a *subset* of ML that uses neural networks with many layers ("deep" = many layers). This is what powers image recognition, speech recognition, and large language models.

```
AI  ⊃  Machine Learning  ⊃  Deep Learning
```

So: every LLM is deep learning, every deep learning system is machine learning, every machine learning system is AI — but not the other way around.

### What is Generative AI?

Generative AI is a category of AI models that **create new content** (text, images, audio, code) rather than just classifying or predicting a number. A model that labels an email "spam/not spam" is *not* generative. A model that writes a new email from scratch *is* generative. ChatGPT, Midjourney, and GitHub Copilot are all generative AI.

### What is an LLM?

LLM = **Large Language Model**. It's a deep learning model trained on huge amounts of text to predict "what word comes next" given the words before it. That simple next-word-prediction task, done at massive scale, is enough to make the model capable of conversation, summarization, coding, translation, and more.

Key idea: an LLM doesn't "know" facts the way a database does — it generates the statistically most likely continuation of text based on patterns seen during training. That's why LLMs can sound confident while being wrong (this is called "hallucination").

### ChatGPT vs API — what's the difference?

- **ChatGPT** is a *product* — a chat website/app built on top of an LLM, with a UI, memory, and safety layers already wired up for you.
- **The API** is the *raw model access* — you send it text, it sends text back, and you build whatever interface you want around it (a CLI, a web app, a Slack bot, etc.).

Think of it like: ChatGPT is a restaurant meal, the API is the raw ingredients you cook with yourself. Today, you're using the ingredients.

### What is an API?

**API = Application Programming Interface.** It's a defined way for your code to talk to someone else's service over the internet. You send a request (with your question and settings), their server processes it, and sends back a response — usually as JSON.

You don't need to know *how* the LLM works internally to use its API — you just need to know the "contract": what to send, what you'll get back.

### What is an SDK?

**SDK = Software Development Kit.** It's a package (library) that wraps the raw API calls in convenient functions, so you don't have to manually build HTTP requests yourself. For example, instead of writing raw HTTP code, you write:

```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(...)
```

The SDK handles the HTTP request, authentication headers, and response parsing for you.

### API Key

An **API key** is a secret string that identifies *you* (or your app) to the provider, so they know who to bill and can enforce rate limits. It's like a password — anyone who has your key can use your account and run up your bill. That's why it's **never** hardcoded in source code or committed to GitHub — it lives in a `.env` file that stays on your machine only (see the Coding Exercise below).

### Client–Server Basics

- **Client** — the program that *sends* a request (your Python script).
- **Server** — the program that *receives* the request, processes it, and sends back a response (OpenAI's servers, in this case).

Every API call today follows this pattern:

```
Your script (client)  ──request (your prompt)──▶  OpenAI server
Your script (client)  ◀──response (AI's reply)───  OpenAI server
```

---

## 🎥 Best Resource

freeCodeCamp – OpenAI API Crash Course (search for the latest available version on YouTube)

## 📚 Reading

[OpenAI API Quickstart](https://platform.openai.com/docs/quickstart) (official docs)

---

## 💻 Coding Exercise

1. **Create the project folder** (already done if you're using this repo structure).
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate # macOS/Linux
   ```
3. **Install the SDK:**
   ```bash
   pip install openai python-dotenv
   ```
4. **Connect the API** — copy `.env.example` to `.env` and paste your real API key into it.
5. **Print your first AI response** — fill in the `TODO(Day 1)` sections in `src/assistant.py`, then run:
   ```bash
   python main.py
   ```

---

## 🛠️ Today's Feature

The assistant replies to one question, end to end: you type a question in the terminal, it's sent to the API, and the reply is printed back.

---

## 🧠 Quiz

1. What's the difference between AI, Machine Learning, and Deep Learning?
2. What makes a model "generative" instead of just predictive?
3. What does an LLM actually predict, one step at a time?
4. Why is ChatGPT not the same thing as "the OpenAI API"?
5. Why should an API key never be committed to GitHub?

*(Answers are in the theory section above — try answering from memory first, then check.)*

## ⭐ Bonus

Try asking the assistant 3 different types of questions (a factual question, a creative request, and a coding question) and compare the responses.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| `Invalid API key` | Wrong key copied, or key has extra spaces | Re-copy the key from your provider's dashboard exactly |
| `.env` not loading | `load_dotenv()` not called, or `.env` in wrong folder | Make sure `.env` is in the project root and `python-dotenv` is installed |
| Wrong Python interpreter | venv not activated | Confirm with `where python` (Windows) that it points inside `venv\Scripts\` |

## ✅ Checklist

- [ ] Environment ready (venv created & activated)
- [ ] SDK installed
- [ ] `.env` created with a real API key
- [ ] API call working
- [ ] First response received and printed
- [ ] Git commit made
