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
# ============================================================

st.markdown("""
<style>
.stApp {
background:
radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.18), transparent 30%),
radial-gradient(circle at 90% 10%, rgba(236, 72, 153, 0.16), transparent 30%),
radial-gradient(circle at 80% 90%, rgba(14, 165, 233, 0.14), transparent 30%),
linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #fdf2f8 100%);
background-attachment: fixed;
}

.block-container {
padding-top: 2rem;
padding-bottom: 2rem;
max-width: 1200px;
}

.main-header {
padding: 28px 32px;
border-radius: 24px;
background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.55));
border: 1px solid rgba(255,255,255,0.8);
box-shadow: 0 15px 45px rgba(15,23,42,0.10);
backdrop-filter: blur(18px);
margin-bottom: 25px;
}

.main-title {
font-size: 42px;
font-weight: 800;
letter-spacing: -1px;
background: linear-gradient(90deg, #4f46e5, #7c3aed, #db2777);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin-bottom: 5px;
}

.main-subtitle {
color: #64748b;
font-size: 17px;
}

.online-status {
display: inline-block;
padding: 7px 14px;
border-radius: 999px;
background: rgba(34,197,94,0.12);
color: #15803d;
font-size: 13px;
font-weight: 600;
margin-top: 12px;
}

.feature-card {
padding: 20px;
border-radius: 18px;
background: rgba(255,255,255,0.65);
border: 1px solid rgba(255,255,255,0.9);
box-shadow: 0 10px 30px rgba(15,23,42,0.07);
backdrop-filter: blur(15px);
min-height: 120px;
transition: all 0.25s ease;
}

.feature-card:hover {
transform: translateY(-4px);
box-shadow: 0 15px 35px rgba(15,23,42,0.12);
}

.feature-icon {
font-size: 30px;
margin-bottom: 8px;
}

.feature-title {
font-weight: 700;
color: #1e293b;
font-size: 16px;
}

.feature-description {
color: #64748b;
font-size: 13px;
margin-top: 5px;
}

.welcome-card {
padding: 25px;
border-radius: 22px;
background: linear-gradient(135deg, rgba(255,255,255,0.78), rgba(255,255,255,0.52));
border: 1px solid rgba(255,255,255,0.9);
box-shadow: 0 12px 35px rgba(15,23,42,0.08);
backdrop-filter: blur(18px);
margin-bottom: 20px;
}

.welcome-title {
font-size: 24px;
font-weight: 750;
color: #1e293b;
margin-bottom: 8px;
}

.welcome-text {
color: #64748b;
font-size: 15px;
}

section[data-testid="stSidebar"] {
background: linear-gradient(180deg, rgba(248,250,252,0.95), rgba(238,242,255,0.95));
border-right: 1px solid rgba(148,163,184,0.15);
}

.sidebar-brand {
font-size: 23px;
font-weight: 800;
color: #312e81;
margin-bottom: 5px;
}

.sidebar-subtitle {
color: #64748b;
font-size: 13px;
margin-bottom: 20px;
}

.sidebar-section {
font-size: 14px;
font-weight: 700;
color: #334155;
margin-top: 20px;
margin-bottom: 10px;
}

.example-question {
padding: 9px 11px;
margin-bottom: 7px;
border-radius: 10px;
background: rgba(255,255,255,0.65);
border: 1px solid rgba(226,232,240,0.8);
color: #475569;
font-size: 12px;
}

[data-testid="stChatMessage"] {
border-radius: 18px;
margin-bottom: 12px;
padding: 5px;
}

[data-testid="stChatInput"] {
border-radius: 18px;
}

.footer {
text-align: center;
color: #94a3b8;
font-size: 12px;
padding: 15px;
}

hr {
border: none;
border-top: 1px solid rgba(148,163,184,0.20);
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

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
Powered by <b>Gemini</b> • <b>Python</b> • <b>Agentic AI</b> • <b>SQLite</b> • <b>Streamlit</b>
</div>
""")

