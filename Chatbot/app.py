import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI

# -----------------------------
# 🔐 Load Environment Variables
# -----------------------------
load_dotenv(".api_key")

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("❌ API Key not found. Check your .api_key file.")
    st.stop()

# -----------------------------
# 📦 Initialize Grok Client (xAI)
# -----------------------------
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.x.ai/v1"   # ✅ Grok endpoint
    )

client = st.session_state.client

# -----------------------------
# 🧠 System Prompt
# -----------------------------
SYSTEM_PROMPT = """You are a professional career advisor chatbot.

Your job is to guide users in their career journey.

Provide:
- Career suggestions based on skills/interests
- Required skills and learning roadmap
- Job roles and salary insights
- Resume and interview tips

Rules:
- Keep answers in 4–6 bullet points
- Be practical and actionable
- Use simple and clear language
- Be friendly and motivating
"""

# -----------------------------
# 💬 Initialize Chat Memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# -----------------------------
# 🖥️ UI CONFIG
# -----------------------------
st.set_page_config(page_title="Career Advisor Bot", page_icon="🎯")

st.title("🎯 Career Advisor Chatbot (Grok)")
st.caption("Get guidance on careers, skills, jobs, and interviews")

# -----------------------------
# 🔄 Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.success("Chat cleared!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Suggested Questions")
    st.write("• Roadmap to become a Data Scientist")
    st.write("• Skills required for Software Developer")
    st.write("• How to crack interviews?")
    st.write("• Career options after B.Tech")

# -----------------------------
# 💬 Display Chat Messages
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# -----------------------------
# ⌨️ User Input
# -----------------------------
user_input = st.chat_input("Ask your career question...")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)
        st.caption(timestamp)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                
                response = client.chat.completions.create(
                    model="grok-2-latest",   # ✅ Grok model
                    messages=st.session_state.messages,
                    temperature=0.7,
                )

                bot_reply = response.choices[0].message.content

                st.write(bot_reply)
                st.caption(timestamp)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_reply
        })

    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg
        })