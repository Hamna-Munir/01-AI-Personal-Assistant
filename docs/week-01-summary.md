# 📅 Week 1 — AI Systems Engineer Bootcamp

**Repository:** `01-AI-Personal-Assistant`
**Theme:** Talking to AI
**Final Goal:** Build AI Personal Assistant v1.0

---

## 🎯 Week Objective

Go from *never having called an LLM API* to shipping a **live, deployed, multi-mode AI Personal Assistant** with structured output, conversation memory, and clean, professional code — in 7 days.

---

## 🗺️ Day-by-Day Recap

| Day | Focus | Objective | Feature Shipped |
|---|---|---|---|
| **1** | AI Fundamentals & Environment Setup | Understand how an LLM works and make your first API call | Assistant replies to one question |
| **2** | Python for AI Projects | Learn only the Python needed for AI engineering | Assistant works using modular code (`main.py`, `assistant.py`, `config.py`) |
| **3** | Prompt Engineering | Control AI responses | Assistant has modes: General Chat, Grammar Fix, Explain, Summarize |
| **4** | Structured Outputs | Make AI produce predictable outputs | Assistant returns structured JSON (title, summary, keywords) |
| **5** | Conversation Memory | Remember previous messages | Assistant remembers the conversation |
| **6** | Clean Code & Refactoring | Turn beginner code into professional code | Professional folder structure and code cleanup |
| **7** | Finalization & Deployment | Ship Version 1.0 | Live AI Personal Assistant, deployed and public |

---

## 🧠 Core Concepts Covered This Week

- **AI / ML / DL** — how the three nest inside each other, and where LLMs fit
- **Generative AI** — models that create content vs. models that classify/predict
- **API vs SDK vs ChatGPT** — raw model access vs. a convenience wrapper vs. a finished product
- **Client–server communication** — how a script talks to a provider's servers over HTTP
- **Modular Python** — functions, imports, and splitting a project into logical files
- **Prompt engineering** — system/user/assistant roles, temperature, tokens, and prompt design
- **Structured outputs** — getting predictable JSON back from a model instead of free-form prose
- **Conversation memory** — how a context window and chat history let an assistant "remember"
- **Clean code practices** — naming, function size, comments, error handling, and basic logging
- **Deployment** — moving an app from "runs on my machine" to a live, publicly reachable link, and why secrets on a deployment platform are separate from a local `.env`

---

## 🛠️ What the Assistant Can Do (v1.0)

By the end of Week 1, the assistant:

- Holds a real conversation and remembers earlier turns
- Switches between multiple modes — General Chat, Grammar Fix, Explain, Summarize, and Structured
- Returns clean structured JSON (title / summary / keywords) on request
- Handles errors gracefully instead of crashing
- Runs from a clean, modular, professional codebase
- Is deployed and reachable via a live link — not just running locally

---

## 📦 Deliverables

- [ ] `README.md` documenting setup, usage, and features
- [ ] Clean, modular project structure (`main.py`, `src/assistant.py`, `config.py`, etc.)
- [ ] `.env.example` (real `.env` never committed)
- [ ] `requirements.txt` up to date
- [ ] Deployed, publicly accessible app link
- [ ] Demo screenshots or video

---

## 🔑 Biggest Lessons of the Week

1. An LLM predicts the next most likely word — it doesn't "know" facts like a database.
2. The API key is a secret, not a variable — it never belongs in committed code.
3. Prompts are a design surface — small wording changes meaningfully change output quality.
4. "Structured" output isn't free — it has to be explicitly requested and validated.
5. Memory is just re-sending prior messages with each request, not the model "remembering" on its own.
6. Clean code isn't a final polish step — it's what makes Day 7's deployment actually possible without surprises.
7. Local and deployed environments are different worlds — what runs on your machine isn't guaranteed to run on the server until dependencies and secrets are handled explicitly.

---

## ➡️ Looking Ahead

Week 1 ends with a working, deployed v1.0. From here, the natural next steps are: adding tool/function calling, persistent (cross-session) memory, a proper user-facing UI beyond the basics, and expanding the assistant's capabilities beyond text-only interactions.
