"""
config.py — Environment & configuration management.

Day 1: loads the API key from .env so it's never hardcoded in source.
Day 2: extracted into its own module as part of the project's modular structure.

Uses Groq (free tier, OpenAI-compatible API) instead of OpenAI — same SDK,
just a different base_url and key, so the rest of the code barely changes.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Copy .env.example to .env and add your free key "
        "from console.groq.com."
    )