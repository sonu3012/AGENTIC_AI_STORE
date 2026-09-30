import streamlit as st

from agent import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Agentic AI Store",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# NOTE: HTML/CSS injected via st.markdown must NOT be indented
# with 4+ leading spaces per line — Streamlit's markdown parser
# treats that as a code block and prints raw tags as text
# instead of rendering them. Keep everything flush-left inside
# the triple-quoted string.
#
# THEME
#   Ink navy  #0F1B33   headers, sidebar, primary text
#   Amber     #F5A524   accent (price-tag / shopping feel)
#   Teal      #14B8A6   online status, focus glow
#   Mist      #F4F7FB   page background
#   Slate     #5B6B85   secondary text
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

:root {
--ink: #0F1B33;
--ink-soft: #1B2B4B;
--amber: #F5A524;
--amber-soft: rgba(245,165,36,0.14);
--teal: #14B8A6;
--mist: #F4F7FB;
--slate: #5B6B85;
--line: rgba(15,27,51,0.08);
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp {
background:
radial-gradient(circle at 8% 0%, rgba(245,165,36,0.10), transparent 32%),
radial-gradient(circle at 95% 8%, rgba(20,184,166,0.10), transparent 30%),
linear-gradient(180deg, #F7F9FC 0%, #EEF3F9 100%);
background-attachment: fixed;
}

header[data-testid="stHeader"] {
background: transparent;
}

footer {
visibility: hidden;
}

.block-container {
padding-top: 2rem;
padding-bottom: 6rem;
max-width: 1100px;
}

.main-header {
position: relative;
overflow: hidden;
padding: 34px 38px;
border-radius: 26px;
background:
radial-gradient(circle at 92% 15%, rgba(245,165,36,0.35), transparent 38%),
radial-gradient(circle at 5% 110%, rgba(20,184,166,0.28), transparent 40%),
linear-gradient(135deg, #0F1B33 0%, #1B2B4B 100%);
border: 1px solid rgba(255,255,255,0.08);
box-shadow: 0 22px 50px rgba(15,27,51,0.22);
margin-bottom: 26px;
}

.main-title {
font-family: 'Bricolage Grotesque', 'DM Sans', sans-serif;
font-size: 44px;
font-weight: 800;
letter-spacing: -1.2px;
line-height: 1.1;
color: #FFFFFF;
margin-bottom: 8px;
}

.main-subtitle {
color: #C5D0E6;
font-size: 17px;
font-weight: 400;
}

.online-status {
display: inline-block;
padding: 7px 15px;
border-radius: 999px;
background: rgba(20,184,166,0.16);
border: 1px solid rgba(20,184,166,0.45);
color: #7CF0E1;
font-size: 13px;
font-weight: 600;
margin-top: 16px;
}

.feature-card {
padding: 22px 22px 20px 22px;
border-radius: 18px;
background: #FFFFFF;
border: 1px solid var(--line);
border-top: 3px solid var(--amber);
box-shadow: 0 8px 24px rgba(15,27,51,0.06);
min-height: 140px;
transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
transform: translateY(-3px);
box-shadow: 0 14px 32px rgba(15,27,51,0.11);
}

.feature-icon {
display: inline-flex;
align-items: center;
justify-content: center;
width: 46px;
height: 46px;
border-radius: 14px;
background: var(--amber-soft);
font-size: 24px;
margin-bottom: 12px;
}

.feature-title {
font-family: 'Bricolage Grotesque', 'DM Sans', sans-serif;
font-weight: 700;
color: var(--ink);
font-size: 17px;
letter-spacing: -0.2px;
}

.feature-description {
color: var(--slate);
font-size: 14px;
line-height: 1.5;
margin-top: 6px;
}

.welcome-card {
padding: 26px 28px;
border-radius: 20px;
background: #FFFFFF;
border: 1px solid var(--line);
border-left: 5px solid var(--amber);
box-shadow: 0 10px 30px rgba(15,27,51,0.06);
margin-bottom: 22px;
}

.welcome-title {
font-family: 'Bricolage Grotesque', 'DM Sans', sans-serif;
font-size: 24px;
font-weight: 700;
letter-spacing: -0.4px;
color: var(--ink);
margin-bottom: 8px;
}

.welcome-text {
color: var(--slate);
font-size: 15px;
line-height: 1.6;
max-width: 70ch;
}

section[data-testid="stSidebar"] {
background: linear-gradient(180deg, #0F1B33 0%, #14264A 100%);
border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li {
color: #D6DFF0;
}

section[data-testid="stSidebar"] hr {
border: none;
border-top: 1px solid rgba(255,255,255,0.10);
}

.sidebar-brand {
font-family: 'Bricolage Grotesque', 'DM Sans', sans-serif;
font-size: 24px;
font-weight: 800;
letter-spacing: -0.5px;
color: #FFFFFF;
margin-bottom: 4px;
}

.sidebar-subtitle {
color: #94A6C6;
font-size: 13px;
margin-bottom: 18px;
}

.sidebar-section {
font-size: 14px;
font-weight: 700;
color: var(--amber);
margin-top: 18px;
margin-bottom: 10px;
}

.example-question {
padding: 10px 12px;
margin-bottom: 8px;
border-radius: 10px;
background: rgba(255,255,255,0.06);
border: 1px solid rgba(255,255,255,0.10);
border-left: 3px solid var(--amber);
color: #D6DFF0;
font-size: 12.5px;
line-height: 1.4;
}

section[data-testid="stSidebar"] .stButton > button {
border-radius: 12px;
background: rgba(255,255,255,0.08);
border: 1px solid rgba(255,255,255,0.18);
color: #FFFFFF;
font-weight: 600;
transition: background 0.2s ease, border-color 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
background: var(--amber);
border-color: var(--amber);
color: var(--ink);
}

[data-testid="stChatMessage"] {
border-radius: 18px;
margin-bottom: 14px;
padding: 14px 16px;
background: #FFFFFF;
border: 1px solid var(--line);
box-shadow: 0 6px 18px rgba(15,27,51,0.05);
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
background: #FFF6E5;
border-color: rgba(245,165,36,0.35);
}

[data-testid="stChatMessage"] p {
color: var(--ink);
line-height: 1.6;
}

[data-testid="stBottom"] > div {
background: transparent;
}

[data-testid="stChatInput"] {
border-radius: 18px;
border: 1px solid rgba(15,27,51,0.14);
background: #FFFFFF;
box-shadow: 0 10px 30px rgba(15,27,51,0.10);
}

[data-testid="stChatInput"]:focus-within {
border-color: var(--teal);
box-shadow: 0 0 0 3px rgba(20,184,166,0.18), 0 10px 30px rgba(15,27,51,0.10);
}

.footer {
text-align: center;
color: #7A889F;
font-size: 12.5px;
padding: 18px;
}

.footer b {
color: var(--ink-soft);
}

hr {
border: none;
border-top: 1px solid var(--line);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SMALL HTML HELPERS
# Keeping these as one-liners (or flush-left blocks) avoids the
# 4-space code-block trap entirely, and stops the repetition
# that made the original file so long.
# ============================================================

def render_html(html: str) -> None:
    """Render an HTML snippet, guaranteed flush-left so Streamlit's
    markdown parser doesn't mistake it for a code block."""
    st.markdown(html.strip(), unsafe_allow_html=True)


def feature_card(icon: str, title: str, description: str) -> str:
    return (
        f'<div class="feature-card">'
        f'<div class="feature-icon">{icon}</div>'
        f'<div class="feature-title">{title}</div>'
        f'<div class="feature-description">{description}</div>'
        f'</div>'
    )


# ============================================================
# API ERROR WARNING
# Shown under the reply when the agent could not get an answer
# from Gemini (for example, when the free daily quota is used up).
# ============================================================

ERROR_PREFIX = "Sorry, the AI service is temporarily unavailable"


def show_api_warning(answer: str) -> None:
    """If the reply is the 'service unavailable' message, explain why."""
    if answer.startswith(ERROR_PREFIX):
        st.warning(
            "⚠️ **This is not a problem with your question.**\n\n"
            "The Gemini API key has most likely reached its **daily free usage limit** "
            "(quota), so it could not generate a response.\n\n"
            "🕒 Please try again after some time, or come back **tomorrow** "
            "when the limit resets."
        )


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_html('<div class="sidebar-brand">🛒 Agentic AI Store</div>')
    render_html('<div class="sidebar-subtitle">Your intelligent shopping assistant</div>')

    st.divider()

    render_html('<div class="sidebar-section">✨ What I can do</div>')
    st.write("📦  Track your order")
    st.write("🔎  Search products")
    st.write("🏷️  Get product details")
    st.write("🧠  Connect multiple tools")

    st.divider()

    render_html('<div class="sidebar-section">💡 Try asking</div>')

    example_questions = [
        "📦 Where is my order ORD-1002?",
        "👟 Show me shoes",
        "🔎 Tell me about product P101",
        "📦 What product is in my order ORD-1002?",
    ]
    for q in example_questions:
        render_html(f'<div class="example-question">{q}</div>')

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

render_html("""
<div class="main-header">
<div class="main-title">🛒 Agentic AI Store</div>
<div class="main-subtitle">Your intelligent AI-powered shopping assistant</div>
<div class="online-status">🟢 AI Assistant Online</div>
</div>
""")


# ============================================================
# WELCOME + FEATURE CARDS (only before the first message)
# ============================================================

if len(st.session_state.messages) == 0:
    render_html("""
<div class="welcome-card">
<div class="welcome-title">👋 Welcome to your AI Store Assistant</div>
<div class="welcome-text">
I can help you track orders, search products, find product information,
and answer your shopping questions using intelligent tool selection.
</div>
</div>
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_html(feature_card(
            "📦", "Order Tracking",
            "Quickly check your order status and expected delivery."
        ))

    with col2:
        render_html(feature_card(
            "👟", "Product Search",
            "Find products using simple natural-language questions."
        ))

    with col3:
        render_html(feature_card(
            "🧠", "Smart AI Reasoning",
            "The agent chooses and chains the right tools automatically."
        ))

    st.write("")


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            show_api_warning(message["content"])


# ============================================================
# CHAT INPUT + PROCESSING
# ============================================================

question = st.chat_input("💬 Ask me about an order or product...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("🤖 AI is thinking..."):
            answer = run_agent(question)
        st.markdown(answer)
        show_api_warning(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
Powered by <b>Gemini</b> • <b>Python</b> • <b>Agentic AI</b> • <b>SQLite</b> • <b>Streamlit</b>
</div>
""")

