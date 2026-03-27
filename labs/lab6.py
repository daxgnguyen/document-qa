import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=st.secrets["openai_api_key"])

class ResearchSummary(BaseModel):
    main_answer: str
    key_facts: list[str]
    source_hint: str

st.title("Research Assistant")
st.write("Ask any question and get a helpful research-oriented answer!")
st.caption("Web search enabled — answers can include up-to-date information and cited sources.")

with st.sidebar:
    structured = st.checkbox("Return structured summary")

question = st.text_input("Your question:")

if question:
    if structured:
        response = client.responses.parse(
            model="gpt-4o",
            instructions="You are a helpful research assistant. Cite your sources.",
            input=question,
            tools=[{"type": "web_search_preview"}],
            previous_response_id=st.session_state.get("last_response_id"),
            text_format=ResearchSummary
        )
        st.session_state.last_response_id = response.id
        result = response.output_parsed
        st.write(result.main_answer)
        st.write("**Key Facts:**")
        for fact in result.key_facts:
            st.write(f"- {fact}")
        st.caption(result.source_hint)
    else:
        response = client.responses.create(
            model="gpt-4o",
            instructions="You are a helpful research assistant. Cite your sources.",
            input=question,
            tools=[{"type": "web_search_preview"}],
            previous_response_id=st.session_state.get("last_response_id")
        )
        st.session_state.last_response_id = response.id
        st.write(response.output_text)

    followup = st.text_input("Ask a follow-up question:")

    if followup:
        if structured:
            followup_response = client.responses.parse(
                model="gpt-4o",
                input=followup,
                tools=[{"type": "web_search_preview"}],
                previous_response_id=st.session_state.last_response_id,
                text_format=ResearchSummary
            )
            st.session_state.last_response_id = followup_response.id
            result = followup_response.output_parsed
            st.write(result.main_answer)
            st.write("**Key Facts:**")
            for fact in result.key_facts:
                st.write(f"- {fact}")
            st.caption(result.source_hint)
        else:
            followup_response = client.responses.create(
                model="gpt-4o",
                input=followup,
                tools=[{"type": "web_search_preview"}],
                previous_response_id=st.session_state.last_response_id
            )
            st.session_state.last_response_id = followup_response.id
            st.write(followup_response.output_text)
