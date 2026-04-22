import os
import streamlit as st
from src.ingest import ingest

if "collection" not in st.session_state:
    with st.spinner("Setting up knowledge base..."):
        st.session_state.collection = ingest()

from src.query import ask

st.set_page_config(page_title="Ask Christian", page_icon="🤖")

st.title("Ask Christian 🤖")
st.markdown("An AI assistant that knows everything about Christian Grøtteland. Ask me anything about his skills, experience or projects.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something about Christian..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask(prompt, st.session_state.collection)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})