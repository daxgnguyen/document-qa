import streamlit as st
import json
import os
from openai import OpenAI

st.title("Chatbot with Long-Term Memory")

# Load/save memories
def load_memories():
    if os.path.exists("memories.json"):
        return json.load(open("memories.json"))
    return []

def save_memories(memories):
    json.dump(memories, open("memories.json", "w"))

memories = load_memories()

# Sidebar
st.sidebar.header("Memories")
if memories:
    for m in memories:
        st.sidebar.write(f"- {m}")
else:
    st.sidebar.write("No memories yet. Start chatting!")

if st.sidebar.button("Clear memories"):
    save_memories([])
    st.rerun()

# Client
if "client" not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets["openai_api_key"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = st.session_state.client
    system = "You are a helpful assistant. Things you remember about the user: " + str(memories)

    stream = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "system", "content": system}] + st.session_state.messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Extract new memories
    try:
        extraction = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": f"Existing memories: {memories}\nUser said: {prompt}\nReturn a JSON list of NEW facts about the user (name, preferences, etc). Return [] if none."}],
        )
        new_facts = json.loads(extraction.choices[0].message.content)
        if new_facts:
            save_memories(memories + new_facts)
            st.rerun()
    except Exception:
        pass
