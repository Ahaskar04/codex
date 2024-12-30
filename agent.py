import streamlit as st
import requests
from phi.agent import Agent
from phi.model.openai import OpenAIChat
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
sambanova_api_key = os.getenv("SAMBANOVA_API_KEY")

# Initialize session state for memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "stackoverflow_results" not in st.session_state:
    st.session_state.stackoverflow_results = []

def fetch_stackoverflow(query):
    base_url = "https://api.stackexchange.com"
    path_url = f"/2.3/search/advanced?order=desc&sort=activity&q={query}&site=stackoverflow"
    url = base_url + path_url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "title": item["title"],
                    "link": item["link"],
                    "is_answered": item["is_answered"],
                    "score": item["score"],
                    "body": item.get("body", "")
                }
                for item in data.get("items", [])
            ]
        else:
            return f"Error fetching Stack Overflow data: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_code_with_context(query, stackoverflow_answers):
    # Get conversation history
    conversation_context = ""
    if st.session_state.conversation:
        # Get last 3 conversations for context
        recent_convos = st.session_state.conversation[-3:]
        conversation_context = "\n".join([
            f"User: {convo['user']}\nResponse: {convo['response']}\n"
            for convo in recent_convos
        ])

    # Format Stack Overflow context
    stackoverflow_context = "\n".join([
        f"Answer from Stack Overflow:\nTitle: {answer['title']}\nLink: {answer['link']}\nScore: {answer['score']}"
        for answer in stackoverflow_answers[:3]
    ])

    # Construct the complete prompt
    complete_prompt = f"""
Previous Conversations:
{conversation_context}

Current User Query:
{query}

Relevant Stack Overflow Solutions:
{stackoverflow_context}

Please provide a complete solution considering the user's query, previous conversations, and the Stack Overflow answers above.
"""

    # Generate response using SambaNova
    client = openai.OpenAI(
        api_key=sambanova_api_key,
        base_url="https://api.sambanova.ai/v1",
    )
    response = client.chat.completions.create(
        model='Qwen2.5-Coder-32B-Instruct',
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant that provides complete solutions based on user queries, conversation history, and Stack Overflow information."},
            {"role": "user", "content": complete_prompt}
        ],
        temperature=0.1,
        top_p=0.1
    )
    return response.choices[0].message.content

def handle_submit():
    if st.session_state.input_text.strip():
        try:
            query = st.session_state.input_text

            # First fetch Stack Overflow answers
            stackoverflow_answers = fetch_stackoverflow(query)
            st.session_state.stackoverflow_results = stackoverflow_answers[:3]

            # Generate response with all context
            response = generate_code_with_context(query, stackoverflow_answers)

            # Append to conversation history
            st.session_state.conversation.append({
                "user": query,
                "response": response
            })

            # Reset the input text
            st.session_state.input_text = ""
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Set page config to expand the layout
st.set_page_config(layout="wide")

# Title at the top
st.title("Coding Assistant")

# Create main containers
history_container = st.container()
current_response_container = st.container()
stackoverflow_container = st.container()
input_container = st.container()

# Input container at the bottom
with input_container:
    st.write("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.text_input(
            "Ask your question:",
            key="input_text",
            label_visibility="collapsed",
            on_change=handle_submit
        )
    
    with col2:
        st.button("Submit", on_click=handle_submit, use_container_width=True)

# Display current response (if any) above the input
with current_response_container:
    if st.session_state.conversation:
        latest = st.session_state.conversation[-1]
        st.write("### Current Response")
        st.write(f"**User Query:** {latest['user']}")
        st.code(latest['response'], language="python")

# Display Stack Overflow results
with stackoverflow_container:
    if st.session_state.stackoverflow_results:
        st.write("### Relevant Stack Overflow Solutions")
        for result in st.session_state.stackoverflow_results:
            st.markdown(f"**{result['title']}**")
            st.markdown(f"[View Question]({result['link']})")
            st.write(f"Answered: {result['is_answered']}, Score: {result['score']}")
            st.write("---")

# Display conversation history at the top
with history_container:
    if len(st.session_state.conversation) > 1:  # More than just the latest response
        st.write("### Previous Conversations")
        for turn in reversed(st.session_state.conversation[:-1]):
            st.write(f"**User Query:** {turn['user']}")
            st.code(turn['response'], language="python")
            st.write("---")
