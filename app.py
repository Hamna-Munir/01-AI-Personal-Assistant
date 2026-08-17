"""
app.py — Streamlit UI (Day 7: Finalization & Deployment)

The polished front end for the Week 1 AI Personal Assistant. Wraps
everything built across the week — modes (Day 3), structured output
(Day 4), conversation memory (Day 5), and clean/error-handled code (Day 6)
— into a deployable chat interface.

Run locally:
    streamlit run app.py

Deploy: push to GitHub, then deploy on Streamlit Community Cloud, pointing
at this file. Remember to set GROQ_API_KEY as a "Secret" in the Streamlit
Cloud app settings (never commit your real .env).
"""

import streamlit as st

from src.assistant import ask, ask_structured, format_reply, MODES

# ==============================================================================
# Page config
# ==============================================================================
st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# Mode metadata (icon + short description shown as a badge/caption)
# ==============================================================================
MODE_META = {
    "grammar": {"icon": "✏️", "label": "Grammar", "desc": "Fixes grammar & phrasing"},
    "explain": {"icon": "🧠", "label": "Explain", "desc": "Breaks concepts down simply"},
    "summarize": {"icon": "📄", "label": "Summarize", "desc": "Condenses a passage"},
    "structured": {"icon": "🗂️", "label": "Structured", "desc": "Returns JSON, not prose"},
}

# ==============================================================================
# Professional styling — refined palette, typography, motion & layout
# NOTE: everything inside <style> is kept as ONE continuous block with
# NO blank lines. Streamlit's markdown parser follows CommonMark, which
# terminates a raw-HTML block on the first blank line — if that happens
# here, the remaining CSS gets printed as plain text on the page instead
# of being applied as styling.
# ==============================================================================
_FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)
st.markdown(_FONT_LINKS, unsafe_allow_html=True)

_CSS = """
<style>
:root {
    --accent: #7C6CF6;
    --accent-2: #5B8DEF;
    --accent-soft: rgba(124, 108, 246, 0.14);
    --bg: #0B0D13;
    --bg-gradient: radial-gradient(1200px 600px at 50% -10%, #171A2B 0%, #0B0D13 55%);
    --panel: #12141D;
    --panel-2: #161925;
    --border: #23273A;
    --border-soft: #1B1E2C;
    --text: #F1F2F8;
    --text-muted: #8B90A8;
    --text-faint: #5B6079;
    --success: #4ADE80;
    --shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
}
html, body, .stApp {
    background: var(--bg-gradient) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text);
}
#MainMenu, footer, [data-testid="stHeader"] { visibility: hidden; height: 0; }
[data-testid="stSidebar"] { display: none; }
.block-container { max-width: 800px; padding-top: 2.4rem; padding-bottom: 6rem; }
.app-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.35rem;
}
.app-title-wrap { display: flex; align-items: center; gap: 0.7rem; }
.app-logo {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.25rem; box-shadow: 0 4px 18px rgba(124, 108, 246, 0.35);
}
.app-title {
    font-size: 1.45rem; font-weight: 800; color: var(--text);
    letter-spacing: -0.02em; line-height: 1.15;
}
.app-subtitle { font-size: 0.82rem; color: var(--text-muted); font-weight: 500; }
.status-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: var(--panel-2); border: 1px solid var(--border);
    padding: 0.32rem 0.75rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; color: var(--text-muted);
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--success);
    box-shadow: 0 0 8px rgba(74, 222, 128, 0.7);
}
.header-divider {
    height: 1px; background: linear-gradient(90deg, var(--border) 0%, transparent 100%);
    margin: 1.1rem 0 1.3rem 0;
}
.controls-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1rem 1.1rem 0.3rem 1.1rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}
.stSelectbox div[data-baseweb="select"] > div {
    background: var(--panel-2) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}
[data-testid="stWidgetLabel"] p {
    font-size: 0.68rem !important; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--text-faint) !important; font-weight: 700 !important;
}
.mode-caption {
    font-size: 0.8rem; color: var(--text-muted);
    display: flex; align-items: center; gap: 0.4rem;
    padding: 0.6rem 0.1rem 0.9rem 0.1rem;
}
div.stButton > button {
    background: var(--panel-2); color: var(--text);
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    font-weight: 600; font-size: 0.85rem; padding: 0.55rem 1rem;
    transition: all 0.15s ease;
}
div.stButton > button:hover {
    background: rgba(124, 108, 246, 0.12);
    border-color: var(--accent);
    color: var(--accent-dim, #A79EFB);
}
[data-testid="stChatMessage"] {
    background: var(--panel); border: 1px solid var(--border-soft);
    border-radius: var(--radius-md); box-shadow: var(--shadow);
    padding: 0.2rem 0.3rem; margin-bottom: 0.6rem;
}
[data-testid="stChatMessageContent"] p { color: var(--text); line-height: 1.55; }
[data-testid*="Avatar"] { display: none !important; }
.msg-row { display: flex; align-items: flex-start; gap: 0.7rem; }
.msg-badge {
    flex-shrink: 0; width: 38px; height: 38px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; box-shadow: 0 3px 12px rgba(0, 0, 0, 0.35);
}
.msg-badge.user { background: linear-gradient(135deg, #FF5A5F 0%, #E1306C 100%); }
.msg-badge.assistant { background: linear-gradient(135deg, #FDB813 0%, #F97316 100%); }
.msg-body { flex: 1; padding-top: 0.15rem; }
[data-testid="stChatInput"] textarea {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text) !important;
}
[data-testid="stChatInput"] {
    border-radius: var(--radius-md) !important;
}
[data-testid="stJson"] {
    background: var(--panel-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.empty-state {
    background: var(--panel); border: 1px dashed var(--border);
    border-radius: var(--radius-lg); padding: 1.6rem 1.4rem;
    text-align: center; margin-top: 1rem;
}
.empty-state-emoji { font-size: 1.8rem; margin-bottom: 0.5rem; }
.empty-state-title { font-weight: 700; font-size: 1rem; color: var(--text); margin-bottom: 0.3rem; }
.empty-state-desc { font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; max-width: 460px; margin: 0 auto; }
.empty-state-desc b { color: var(--accent-dim, #A79EFB); }
[data-testid="stCaptionContainer"] { color: var(--text-faint) !important; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 8px; }
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)

# ==============================================================================
# Session state
# ==============================================================================
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": ..., "content": ...}


class _SessionMemory:
    """Thin adapter so src.assistant.ask() can read/write straight into
    Streamlit's session_state without needing its own separate object."""

    def add(self, role: str, content: str) -> None:
        st.session_state.history.append({"role": role, "content": content})

    def as_messages(self, system_prompt: str) -> list:
        return [{"role": "system", "content": system_prompt}, *st.session_state.history]


memory = _SessionMemory()

# ==============================================================================
# Header
# ==============================================================================
st.markdown("""
<div class="app-header">
    <div class="app-title-wrap">
        <div class="app-logo">💬</div>
        <div>
            <div class="app-title">AI Personal Assistant</div>
            <div class="app-subtitle">Week 1 · AI Systems Engineer Bootcamp</div>
        </div>
    </div>
    <div class="status-pill"><span class="status-dot"></span>Groq · Online</div>
</div>
<div class="header-divider"></div>
""", unsafe_allow_html=True)

# ==============================================================================
# Controls
# ==============================================================================
st.markdown('<div class="controls-panel">', unsafe_allow_html=True)
col_mode, col_clear = st.columns([3, 1])
with col_mode:
    mode = st.selectbox(
        "Mode",
        options=list(MODES.keys()) + ["structured"],
        format_func=lambda m: f"{MODE_META.get(m, {}).get('icon', '')}  {m.capitalize()}",
    )
with col_clear:
    st.write("")
    st.write("")
    if st.button("🗑️  Clear chat", use_container_width=True):
        st.session_state.history = []
        st.rerun()

active_meta = MODE_META.get(mode, {"icon": "💬", "desc": ""})
st.markdown(
    f'<div class="mode-caption">{active_meta["icon"]} <b>{mode.capitalize()}</b> — {active_meta["desc"]}</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# Chat history
# ==============================================================================
# Crisp inline SVG icons (instead of emoji) so the avatar renders identically
# across every OS/browser — no more inconsistent emoji font rendering.
_ICON_USER = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="12" cy="8" r="4" fill="white"/>'
    '<path d="M4 20c0-4.4 3.6-8 8-8s8 3.6 8 8" stroke="white" '
    'stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)
_ICON_BOT = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect x="4" y="8" width="16" height="12" rx="3" fill="white"/>'
    '<rect x="9" y="2" width="2" height="4" fill="white"/>'
    '<circle cx="10" cy="1.5" r="1.3" fill="white"/>'
    '<circle cx="9" cy="14" r="1.6" fill="#1B1E2C"/>'
    '<circle cx="15" cy="14" r="1.6" fill="#1B1E2C"/>'
    '<rect x="1" y="12" width="2.4" height="5" rx="1.2" fill="white"/>'
    '<rect x="20.6" y="12" width="2.4" height="5" rx="1.2" fill="white"/>'
    '</svg>'
)


def render_badge_row(role: str) -> None:
    """Renders the colored badge (red badge + person icon for user, amber
    badge + robot icon for assistant) as the opening half of a custom flex
    row; the caller writes the message body right after this inside the
    same st.chat_message block."""
    icon = _ICON_USER if role == "user" else _ICON_BOT
    st.markdown(

        f'<div class="msg-row"><div class="msg-badge {role}">{icon}</div>'
        f'<div class="msg-body">',
        unsafe_allow_html=True,
    )


def close_badge_row() -> None:
    st.markdown('</div></div>', unsafe_allow_html=True)


for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        render_badge_row(turn["role"])
        st.write(turn["content"])
        close_badge_row()

# ==============================================================================
# Input + response
# ==============================================================================
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        render_badge_row("user")
        st.write(user_input)
        close_badge_row()

    with st.chat_message("assistant"):
        render_badge_row("assistant")
        with st.spinner("Thinking..."):
            if mode == "structured":
                try:
                    result = ask_structured(user_input)
                    st.json(result)
                    # Store a readable summary in history rather than raw JSON,
                    # so the chat log stays easy to scan.
                    memory.add("user", user_input)
                    memory.add("assistant", f"(structured result) {result.get('title', '')}")
                except (ValueError, RuntimeError) as e:
                    st.error(str(e))
            else:
                reply = ask(user_input, mode=mode, memory=memory)
                reply = format_reply(reply)
                st.write(reply)
        close_badge_row()

if not st.session_state.history and not user_input:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-emoji">👋</div>
        <div class="empty-state-title">Start a conversation</div>
        <div class="empty-state-desc">
            Ask a question, or switch modes above — <b>Grammar</b> fixes text,
            <b>Explain</b> breaks concepts down simply, <b>Summarize</b> condenses a
            passage, and <b>Structured</b> returns JSON instead of prose.
        </div>
    </div>
    """, unsafe_allow_html=True)