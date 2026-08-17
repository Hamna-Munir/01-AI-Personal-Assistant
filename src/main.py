"""
main.py — CLI entry point for local development.

Run this during Days 1-6 to test the assistant from the terminal before
Day 7 wraps it in a Streamlit UI (see app.py).
"""

from src.assistant import ask, ask_structured, format_reply
from src.memory import ConversationMemory


def main() -> None:
    print("AI Personal Assistant — type 'exit' to quit, 'clear' to reset memory.\n")
    print("Modes: general / grammar / explain / summarize / structured\n")
    memory = ConversationMemory()

    while True:
        mode = input("Mode (press Enter for general): ").strip().lower() or "general"
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "clear":
            memory.clear()
            print("(memory cleared)\n")
            continue

        if mode == "structured":
            # Day 4: returns a dict instead of plain text
            result = ask_structured(user_input)
            print(f"Assistant (JSON): {result}\n")
            continue

        reply = ask(user_input, mode=mode, memory=memory)
        reply = format_reply(reply)
        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()