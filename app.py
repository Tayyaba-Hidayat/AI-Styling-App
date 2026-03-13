import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARIA · AI Assistant",
    page_icon="◈",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 1rem; max-width: 780px; }

/* Background */
.stApp {
    background: #080c10;
    color: #e6edf3;
}

/* Title */
.aria-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    background: linear-gradient(135deg, #00d4aa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0;
}

.aria-subtitle {
    text-align: center;
    color: #7d8590;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
}

/* Mode selector label */
.stSelectbox label {
    color: #7d8590 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 8px !important;
}

/* Chat messages */
.stChatMessage {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
}

/* User message */
[data-testid="stChatMessageContent"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.875rem !important;
    line-height: 1.65 !important;
}

/* Chat input */
.stChatInput {
    border-top: 1px solid #30363d;
    padding-top: 1rem;
}

.stChatInput > div {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
}

.stChatInput textarea {
    font-family: 'Space Mono', monospace !important;
    color: #e6edf3 !important;
    background: transparent !important;
}

.stChatInput textarea::placeholder {
    color: #484f58 !important;
}

/* Buttons */
.stButton > button {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #7d8590 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.15s !important;
}

.stButton > button:hover {
    border-color: #f85149 !important;
    color: #f85149 !important;
    background: rgba(248,81,73,0.05) !important;
}

/* Divider */
hr { border-color: #30363d !important; }

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,212,170,0.08);
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    color: #00d4aa;
    letter-spacing: 0.05em;
}

.dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00d4aa;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Mode badge colors */
.mode-coder   { color: #79c0ff; border-color: rgba(121,192,255,0.3); background: rgba(121,192,255,0.06); }
.mode-creative { color: #d2a8ff; border-color: rgba(210,168,255,0.3); background: rgba(210,168,255,0.06); }
.mode-analyst  { color: #ffa657; border-color: rgba(255,166,87,0.3);  background: rgba(255,166,87,0.06); }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
MODES = {
    "◈  Assistant": {
        "prompt": "You are ARIA, a helpful, friendly, and knowledgeable AI assistant. Be concise but thorough.",
        "class": "status-badge",
    },
    "⟨/⟩  Coder": {
        "prompt": "You are ARIA, an expert software engineer. Help with code, debugging, and architecture. Always provide clean, well-commented code examples.",
        "class": "status-badge mode-coder",
    },
    "✦  Creative": {
        "prompt": "You are ARIA, a creative writing partner with a vivid imagination. Help with storytelling, brainstorming, and poetry. Be expressive and inspiring.",
        "class": "status-badge mode-creative",
    },
    "⬡  Analyst": {
        "prompt": "You are ARIA, a sharp analytical thinker. Break down complex topics, provide structured reasoning, pros/cons, and data-driven insights.",
        "class": "status-badge mode-analyst",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = list(MODES.keys())[0]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="aria-title">◈ ARIA</div>', unsafe_allow_html=True)
st.markdown('<div class="aria-subtitle">AI ASSISTANT · POWERED BY CLAUDE</div>', unsafe_allow_html=True)

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ◈ ARIA Settings")
    st.markdown("---")

    mode = st.selectbox(
        "MODE",
        options=list(MODES.keys()),
        index=list(MODES.keys()).index(st.session_state.mode),
    )
    st.session_state.mode = mode

    st.markdown("---")
    st.markdown("**About**")
    st.markdown(
        "<small style='color:#7d8590'>ARIA is your personal AI assistant powered by Claude Sonnet. Switch modes to change how it thinks and responds.</small>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("✕  Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#484f58'>Built with Streamlit + Anthropic API</small>",
        unsafe_allow_html=True,
    )

# ── Status bar ────────────────────────────────────────────────────────────────
current_mode_class = MODES[st.session_state.mode]["class"]
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(
        f'<span class="{current_mode_class}"><span class="dot"></span> ONLINE</span>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<small style="color:#484f58;font-size:0.75rem">Mode: {st.session_state.mode.strip()}</small>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Chat history ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align:center;padding:2rem 0;color:#484f58;">
            <div style="font-size:2.5rem;margin-bottom:0.5rem;">◈</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;color:#7d8590;margin-bottom:0.5rem;">How can I help you today?</div>
            <div style="font-size:0.75rem;">Ask me anything — type below to start</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for msg in st.session_state.messages:
    avatar = "◈" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Message ARIA..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Stream AI response
    with st.chat_message("assistant", avatar="◈"):
        system_prompt = MODES[st.session_state.mode]["prompt"]

        try:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            full_response = ""
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=api_messages,
            ) as stream:
                placeholder = st.empty()
                for text in stream.text_stream:
                    full_response += text
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except KeyError:
            st.error(
                "⚠ API key not found. Add ANTHROPIC_API_KEY to your Streamlit secrets. "
                "See the README for instructions.",
                icon="🔑",
            )
        except anthropic.APIError as e:
            st.error(f"⚠ Anthropic API error: {e}", icon="⚠")
