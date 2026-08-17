# Day 7 — Finalization & Deployment

**Objective:** Ship Version 1.0.

---

## 📖 Theory

### README

A `README.md` is the front door of your repository — it's the first (and often only) thing a recruiter, teammate, or future-you reads before deciding whether the project is worth a second look. A strong README answers, in order: *what is this, why does it exist, how do I run it, what does it look like.*

A solid structure to follow:

```
# Project Title
One-line description of what it does and who it's for.

## Features
- Bullet list of what the assistant can do (modes, structured output, memory, etc.)

## Demo / Screenshot
An image or GIF is worth a thousand words of description.

## Tech Stack
Python · Streamlit · Groq API · python-dotenv

## Setup
Step-by-step: clone, venv, install, .env, run.

## Usage
How to actually interact with it once it's running.

## Project Structure
A short tree of the important files/folders.

## What I Learned
A few sentences on the specific skills this project proved.
```

Keep it scannable — short paragraphs, code blocks for anything runnable, and a screenshot near the top. Nobody reads a wall of text before they've seen what the thing does.

### GitHub Portfolio

Your GitHub profile is a portfolio whether you curate it or not — so curate it. A few habits that make a repository look "finished" rather than abandoned mid-tutorial:

- **Meaningful commit history.** A trail of `wip`, `fix`, `asdf` commits signals an unfinished experiment. A clean history of scoped commits (`Add structured output mode`, `Fix memory reset bug`) signals a maintained project.
- **A pinned repo + updated profile README.** GitHub lets you pin your best repos and write a profile-level `README.md` that shows on your profile page — use both.
- **No secrets committed.** A `.env` file, an API key, or a `venv/` folder in your commit history is an instant red flag to anyone reviewing your code. `.gitignore` should already be excluding these (see Day 6 checklist) — Day 7 is your last chance to verify with `git status` before it goes public.
- **License + short description.** Even a one-line repo description and an MIT license make a repo look intentional rather than incidental.

### Deployment Basics

"Deployment" just means moving your app from *running on your machine* to *running somewhere anyone with a link can reach*. For a Streamlit app, the simplest path is **Streamlit Community Cloud**, which is free and built specifically for this:

1. Push your project to a **public GitHub repository** (private repos need a paid plan on some platforms).
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
3. Point it at your repo, branch, and the entry file (`app.py`).
4. Add your secrets — this is the part people get wrong. Your `.env` file **never** gets pushed to GitHub, so the deployed app has no idea what your API key is until you tell the platform directly. On Streamlit Cloud this lives under **App settings → Secrets**, where you paste the same key="value" pairs your `.env` has locally.
5. Deploy. The platform installs everything from `requirements.txt` and starts your app — if a package is missing from that file, deployment will fail even though it worked locally (see Common Errors below).

The core idea that trips people up: **your local `.env` and the platform's "Secrets" are two separate, disconnected places.** Updating one does nothing to the other.

---

## 🎥 Best Resource

Streamlit deployment tutorial (or chosen deployment platform)

## 📚 Reading

[GitHub README guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

---

## 💻 Coding Exercise

Deploy the assistant.

1. **Finalize `requirements.txt`** — make sure every package your app imports is listed with a pinned or minimum version.
2. **Write the README** — using the structure above, document what the assistant does and how to run it.
3. **Double-check `.gitignore`** — confirm `.env` and `venv/` are excluded (`git status` should show neither as trackable).
4. **Push to GitHub** — commit everything, push to a public repo.
5. **Deploy** — connect the repo on Streamlit Community Cloud (or your chosen platform), add `GROQ_API_KEY` as a Secret, and deploy.
6. **Test the live link** — open the deployed URL in a fresh/incognito browser tab and run through every mode to confirm it behaves exactly like it did locally.

---

## 🛠️ Today's Feature

Live AI Personal Assistant.

---

## 🧠 Quiz

Review of the week.

1. What's the difference between AI, ML, and Deep Learning? (Day 1)
2. What's the difference between a chat mode and structured output? (Day 3–4)
3. How does the assistant "remember" earlier turns in a conversation? (Day 5)
4. Why do we wrap API calls in `try/except` instead of letting errors crash the app? (Day 6)
5. Why does deploying an app require setting Secrets separately from your local `.env`?

*(Answers are drawn from each day's theory section — try answering from memory first, then check back.)*

## ⭐ Bonus

Record a demo video.

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Missing dependencies | A package works locally (already installed in your venv) but isn't listed in `requirements.txt` | Run `pip freeze > requirements.txt` from an activated, clean venv before pushing |
| Environment variables on deployment | The app works locally but crashes on the deployed link with an auth/key error | Add the same key="value" pairs from your `.env` into the platform's "Secrets" settings — local `.env` files are never uploaded |
| App builds but shows a blank/error page | Wrong entry-point file specified, or an import path assumes a local folder structure that isn't present after deployment | Confirm the entry file is `app.py` and all imports use relative paths from the repo root |
| Works locally, breaks after deploy for no obvious reason | Python version mismatch between your machine and the deployment platform | Pin a `python_version` (e.g. in `runtime.txt` or platform settings) to match what you tested locally |

## ✅ Checklist

- [ ] README complete
- [ ] Screenshots added
- [ ] Notes complete
- [ ] Week summary complete
- [ ] Deployment successful
- [ ] GitHub updated
