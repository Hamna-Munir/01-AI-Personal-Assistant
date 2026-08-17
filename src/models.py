"""
models.py — Typed data models used across the project.

Two kinds of structure live here:
  1. `Message`      — one turn in a conversation (Day 5: Conversation Memory)
  2. `StructuredOutput` — the shape of the JSON the assistant returns in
     "structured" mode (Day 4: Structured Outputs), validated with Pydantic
     so a malformed model response fails loudly and predictably instead of
     silently breaking the UI.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Literal

from pydantic import BaseModel, Field, field_validator

Role = Literal["system", "user", "assistant"]


# ==============================================================================
# Conversation memory (Day 5)
# ==============================================================================
@dataclass
class Message:
    """One turn in a conversation.

    Kept as a plain dataclass (not Pydantic) because this is created and
    read constantly in a hot loop (every chat turn) and doesn't need
    external-input validation — it's produced by our own code, not parsed
    from an API response.
    """

    role: Role
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_api_message(self) -> dict:
        """Shape expected by the chat completions API — just role + content,
        no timestamp (the API doesn't need it, and some providers reject
        unknown keys)."""
        return {"role": self.role, "content": self.content}


# ==============================================================================
# Structured output (Day 4)
# ==============================================================================
class StructuredOutput(BaseModel):
    """Validated shape of a "structured" mode response.

    Using Pydantic here (rather than a dataclass) because this data comes
    from the model's raw text output — it needs real validation, not just
    a type hint, since an LLM can return malformed or incomplete JSON.
    """

    title: str = Field(..., min_length=1, max_length=120)
    summary: str = Field(..., min_length=1)
    keywords: List[str] = Field(..., min_length=1, max_length=10)

    @field_validator("keywords")
    @classmethod
    def _no_empty_keywords(cls, value: List[str]) -> List[str]:
        cleaned = [kw.strip() for kw in value if kw and kw.strip()]
        if not cleaned:
            raise ValueError("keywords list cannot be empty after cleaning")
        return cleaned

    class Config:
        # Reject unexpected extra fields instead of silently dropping them —
        # if the model starts returning a different shape, we want to know.
        extra = "forbid"
