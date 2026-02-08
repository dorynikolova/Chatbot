import streamlit as st
from chatbot import ask_bilbo

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Bilbo Baggins",
    page_icon="📚",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #7b2cbf !important; 
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.user-bubble {
    background-color: #e0e0e0;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 80%;
}

.bilbo-bubble {
    background-color: #d0b3ff;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 80%;
}
            
.thinking-bubble {
    background-color: #cbb2ff;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 80%;
    font-style: italic;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📚 Bilbo Baggins")
    st.write("Your friendly multilingual Spanish study companion.")
    st.write("Warm, academic, motivating and a little goofy.")
    st.markdown("---")
    st.write("Made by Doroteya 💛")

# --- MAIN CHAT UI ---
st.title("💬 Chat with Bilbo")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state: 
    st.session_state.user_input = ""

# previous messages
#for msg in st.session_state.messages:
 #   role = "🧑‍🎓 You" if msg["role"] == "user" else "🧙 Bilbo"
  #  st.markdown(f"**{role}:** {msg['content']}")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>🧑‍🎓 {msg['content']}</div>", unsafe_allow_html=True)

    elif msg["content"] == "…":
        st.markdown("<div class='thinking-bubble'>🧙 Bilbo is thinking…</div>", unsafe_allow_html=True)

    else:
        st.markdown(f"<div class='bilbo-bubble'>🧙 {msg['content']}</div>", unsafe_allow_html=True)
    

# --- INPUT FORM ---
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1]) 
    with col1: user_input = st.text_input("Type your message here:", key="user_input") 
    with col2: submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": "…"})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["content"] == "…":
    user_message = st.session_state.messages[-2]["content"]
    real_answer = ask_bilbo(st.session_state.messages)
    st.session_state.messages[-1]["content"] = real_answer
    st.rerun()


