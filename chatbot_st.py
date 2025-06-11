import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# load data from .env
st.code(st.session_state)
load_dotenv("./.env", override=True)
api_key = os.getenv("openrouter_secret")
base_url = os.getenv("base_url")
model = os.getenv("model")

# initialize API connection
client = OpenAI(api_key=api_key, base_url=base_url)

# check for existing messages
if "messages" in st.session_state:
    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
else:
    st.session_state["messages"] = []


if prompt := st.chat_input("Enter your message", key="prompt", accept_file=True):
    # display user message
    with st.chat_message("user"):
        st.markdown(prompt.text)

    # save user message
    st.session_state["messages"].append({"role": "user", "content": prompt.text})

    # generate (stream) llm response
    llm_message = client.chat.completions.create(messages=st.session_state["messages"], model=model, stream=True)

    # display (stream) llm response
    with st.chat_message("assistant"):
        response = st.write_stream(llm_message)

    # save llm response
    st.session_state["messages"].append({"role": "assistant", "content": response})

st.code(st.session_state)
