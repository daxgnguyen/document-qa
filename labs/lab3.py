import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Chatbot")
st.write(
    "Talk to GPT! "
)

# Model selection
use_advanced = st.sidebar.checkbox("Use advanced model")

 # Create an OpenAI client.
if "client" not in st.session_state:
    api_key = st.secrets["openai_api_key"]
    st.session_state.client = OpenAI(api_key=st.secrets["openai_api_key"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant that explains things so a 10 year old can understand. When answering questions: After answering, always ask 'Do you want more info on this?'. If the user says 'yes', provide more details and ask again 'Do you want more info on this?'. If the user says 'No', say 'Okay, what else can I help you with?'"}]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    client = st.session_state.client
    stream = client.chat.completions.create(
        model = "gpt-5-nano" if use_advanced else "gpt-5-mini",
        messages = st.session_state.messages,
        stream=True)
    
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Keep only last 2 user messages and keep system prompt
if len(st.session_state.messages) > 5:
    st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-4:]

