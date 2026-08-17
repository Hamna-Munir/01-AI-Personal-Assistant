"""
memory.py — Conversation memory.

Day 5: a minimal chat-history store so the assistant can remember prior
turns within a session. Kept intentionally simple (a list in memory) —
the goal this week is to understand the *concept* of a context window,
not to build a production memory store.
"""


class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.history: list[dict] = []

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        # Simple truncation to avoid unbounded token growth (concept only —
        # a real implementation would count tokens, not turns).
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def as_messages(self, system_prompt: str) -> list[dict]:
        return [{"role": "system", "content": system_prompt}, *self.history]

    def clear(self) -> None:
        """Bonus (Day 5): a command to reset the conversation."""
        self.history = []