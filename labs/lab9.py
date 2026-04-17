import streamlit as st
import json
import os
from openai import OpenAI

def load_memories():
    if os.path.exists("memories.json"):
        with open("memories.json", "r") as f:
            return json.load(f)
    return[]

def save_memories(memories):
    with open("memories.json", "w") as f:
        json.dump(memories, f)

# Show title and description.
st.title("Chatbot with Memory")
st.write(
    "Talk to GPT and I'll remember who you are! "
)

# Memories Sidebar
st.sidebar.header("Memories")
memories = load_memories()

if memories:
    for memory in memories:
            st.sidebar.write(f"-{memory}")
else:
    st.sidebar.write("No memories yet. Start chatting!")

if st.sidebar.button("Clear all memories"):
    save_memories([])
    st.rerun()

# Model selection
use_advanced = st.sidebar.checkbox("Use advanced model")

 # Create an OpenAI client.
if "client" not in st.session_state:
    api_key = st.secrets["openai_api_key"]
    st.session_state.client = OpenAI(api_key=st.secrets["openai_api_key"])
client = st.session_state.client

system_prompt = (
    "You are a helpful assistant that explains things so a 10 year old can understand. "
    "Here are things you remember about the user from past conversations: "
    f"{memories if memories else 'Nothing yet.'}"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send system prompt + history to LLM
    messages_to_send = [{"role": "system", "content": system_prompt}] + st.session_state.messages
    stream = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages_to_send,
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # ---------- Extract new memories ----------
    extraction_prompt = f"""You analyze conversations to extract NEW facts worth remembering about the user (name, preferences, interests, location, job, etc.).

Existing memories (do NOT duplicate these):
{memories}

User said: {prompt}
Assistant said: {response}

Return ONLY a JSON list of new facts as short strings. If nothing new, return [].
Example: ["lives in Boston", "likes hiking"]"""

    try:
        extraction = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": extraction_prompt}],
        )
        new_facts = json.loads(extraction.choices[0].message.content)
        if new_facts:
            save_memories(memories + new_facts)
            st.rerun()
    except Exception:
        pass

# Trim history (keep last 4 turns)
if len(st.session_state.messages) > 4:
    st.session_state.messages = st.session_state.messages[-4:]
