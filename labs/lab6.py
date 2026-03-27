import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Research Assistant")
st.write("Ask any question and get a helpful research-oriented answer.")

question = st.text_input("Your question:")

if question:
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="You are a helpful research assistant.",
        input=question
    )
    st.write(response.output_text)
