import streamlit as st
import requests

st.set_page_config(page_title="Hospital Agent", page_icon="🩺")
st.title("🩺 Hospital Appointment Assistant")

# Initial greeting
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "Hi, how can I help you today?"}]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 🔁 Call backend (mock or real for now)
    response = requests.post("http://localhost:8000/chat",json={"user_id": "demo_user", "message": prompt})
    reply = response.json()["reply"]

    # Show agent reply
    st.session_state.messages.append({"role": "agent", "content": reply})
    with st.chat_message("agent"):
        st.markdown(reply)