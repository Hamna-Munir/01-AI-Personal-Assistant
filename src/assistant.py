"""
assistant.py — Core assistant logic.

This module grows across the week:
  Day 1: a single function that sends one prompt and returns one response.
  Day 3: multiple "modes" (general chat, grammar fix, explain, summarize),
         each with its own system prompt.
  Day 4: an option to request structured (JSON) output.
  Day 5: conversation memory — the assistant remembers prior turns.

Fill in each section as you complete that day. Placeholders are marked
with TODO(Day N) so it's obvious what belongs where.
"""

from openai import OpenAI
import json

from src.config import GROQ_API_KEY, GROQ_BASE_URL, MODEL_NAME, DEFAULT_TEMPERATURE

# Groq's API is OpenAI-compatible, so we still use the `openai` SDK —
# just pointed at Groq's server instead of OpenAI's.
client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


# ---------------------------------------------------------------------------
# Day 3 — system prompts per mode
# ---------------------------------------------------------------------------
MODES = {
    "general": "You are a helpful, concise assistant.",
    "grammar": "You correct grammar and spelling only. Do not change meaning or tone.",
    "explain": "You explain concepts simply, as if to a beginner, with a short example.",
    "summarize": "You summarize the given text in 3-5 bullet points.",
}


def ask(prompt: str, mode: str = "general", temperature: float = DEFAULT_TEMPERATURE, memory=None) -> str:
    """Day 1 baseline: send one prompt, get one response.

    Day 3 extends this with `mode` to select a system prompt.
    Day 5 extends this further: if a ConversationMemory is passed in, prior
    turns are included so the model has context from earlier in the chat.
    """
    system_prompt = MODES.get(mode, MODES["general"])

    if memory is not None:
        # Day 5: re-send the whole conversation so far, plus the new message
        memory.add("user", prompt)
        messages = memory.as_messages(system_prompt)
    else:
        # Day 1-4 behavior: no memory, just this one exchange
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=temperature,
        messages=messages,
    )
    reply = response.choices[0].message.content

    if memory is not None:
        memory.add("assistant", reply)

    return reply


def ask_structured(text: str) -> dict:
    """Day 4: return structured JSON (title, summary, keywords) instead of
    free-form text, given a block of input text to analyze.
    """
    system_prompt = (
        "You analyze the given text and respond with ONLY valid JSON — "
        "no extra words before or after it. The JSON must have exactly "
        "these three keys: "
        '"title" (a short string), '
        '"summary" (a 1-2 sentence string), '
        '"keywords" (a JSON array of 3-5 short strings).'
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,  # low temperature: we want consistent, predictable JSON
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    raw_reply = response.choices[0].message.content

    try:
        result = json.loads(raw_reply)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw_reply}")

    # Bonus: validate the shape before trusting it
    required_keys = {"title", "summary", "keywords"}
    missing = required_keys - result.keys()
    if missing:
        raise ValueError(f"Response is missing required fields: {missing}")

    return result

def format_reply(reply: str) -> str:
    return reply.strip()