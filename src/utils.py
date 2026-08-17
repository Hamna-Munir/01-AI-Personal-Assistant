"""
utils.py — Small, reusable helper functions shared across the project.

Everything here is a pure, general-purpose utility (Day 6: Clean Code &
Refactoring) — no Streamlit imports, no direct API calls. That separation
keeps this module trivially testable and reusable outside the UI.
"""

import json
import logging
import os
import re
import sys
from typing import Any, Dict


# ==============================================================================
# Logging (Day 6)
# ==============================================================================
def setup_logger(name: str = "assistant", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger that writes to stdout.

    Safe to call multiple times (e.g. once per module) — it won't attach
    duplicate handlers to the same logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s — %(name)s — %(message)s",
                               datefmt="%H:%M:%S")
        )
        logger.addHandler(handler)
        logger.propagate = False

    return logger


logger = setup_logger()


# ==============================================================================
# Environment variables (Day 1)
# ==============================================================================
def require_env(key: str) -> str:
    """Fetch a required environment variable or raise a clear error.

    Used instead of a bare os.environ[key] / os.getenv(key) so a missing
    API key fails with an actionable message instead of a raw KeyError or
    a confusing 401 from the API later on.
    """
    value = os.getenv(key)
    if not value or not value.strip():
        raise RuntimeError(
            f"Missing required environment variable: {key}. "
            f"Add it to your .env file (see .env.example)."
        )
    return value.strip()


# ==============================================================================
# JSON parsing (Day 4: Structured Outputs)
# ==============================================================================
_CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def safe_json_parse(raw_text: str) -> Dict[str, Any]:
    """Parse a model's raw text response into a JSON dict.

    Models frequently wrap JSON in ```json ... ``` code fences even when
    told not to — this strips those before parsing, and raises a clear
    ValueError (not a raw JSONDecodeError) on genuinely invalid output so
    callers can catch one predictable exception type.
    """
    cleaned = _CODE_FENCE_RE.sub("", raw_text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Model did not return valid JSON: {exc}. Raw output: {raw_text[:200]!r}"
        ) from exc


# ==============================================================================
# Text helpers
# ==============================================================================
def truncate_text(text: str, max_chars: int = 4000) -> str:
    """Trim overly long input before sending it to the API — a basic guard
    against blowing the context window (Day 5) on a single oversized paste."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"
