import streamlit as st
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


# Initialize chatbot
@st.cache_resource
def get_chatbot():
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key="<api_key>",
        model_name="openai/gpt-4.1",
    )
    return ConversationChain(llm=llm, memory=ConversationBufferMemory())


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chatbot = get_chatbot()

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle input
if prompt := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    response = chatbot.predict(input=prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    st.rerun()
