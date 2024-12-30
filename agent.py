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

from urllib.parse import quote

from urllib.parse import quote, urlencode

def fetch_stackoverflow(query):
    base_url = "https://api.stackexchange.com"
    
    # If the query is too long or looks like code, extract keywords
    if len(query) > 150 or '\n' in query:
        # Extract basic keywords if it's a code snippet
        keywords = "python " + " ".join([
            word for word in query.replace('\n', ' ')
                              .replace('(', ' ')
                              .replace(')', ' ')
                              .replace('{', ' ')
                              .replace('}', ' ')
                              .replace(':', ' ')
                              .split()
            if not word.startswith(('import', 'from', 'def', '#'))
            and not word in ['=', '+', '-', '*', '/', '%', '^']
            and len(word) > 2
        ])[:100]  # Limit length
    else:
        keywords = query

    # Use the original working URL structure
    path_url = f"/2.3/search/advanced?order=desc&sort=activity&q={keywords}&site=stackoverflow"
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
            st.error(f"Error fetching Stack Overflow data: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []


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
        st.text_area(
            "Ask your question:",
            key="input_text",
            label_visibility="collapsed",
            height=150,  # Set a fixed height for the text area
            placeholder="Enter your code or question here...",
            help="Press Ctrl+Enter to submit"
        )
    
    with col2:
        # Align button to the top of the column to match text area
        st.write("")  # Add some spacing
        submit_button = st.button(
            "Submit", 
            on_click=handle_submit, 
            use_container_width=True,
            type="primary"  # Make the button more prominent
        )

# Add some CSS to style the text area
st.markdown("""
    <style>
        /* Style the text area */
        .stTextArea textarea {
            font-family: monospace;
            line-height: 1.4;
            padding: 10px;
            white-space: pre;
            overflow-x: auto;
        }
        
        /* Ensure code maintains formatting */
        .stTextArea textarea {
            word-wrap: normal !important;
            overflow-x: scroll !important;
        }
        
        /* Make the text area border more visible */
        .stTextArea textarea {
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        
        /* Add hover effect */
        .stTextArea textarea:hover {
            border-color: #999;
        }
        
        /* Add focus effect */
        .stTextArea textarea:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 0 1px #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

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
        if isinstance(st.session_state.stackoverflow_results, list):  # Verify it's a list
            for result in st.session_state.stackoverflow_results:
                if isinstance(result, dict):  # Verify each item is a dictionary
                    st.markdown(f"**{result.get('title', 'No title')}**")
                    st.markdown(f"[View Question]({result.get('link', '#')})")
                    st.write(f"Answered: {result.get('is_answered', 'N/A')}, Score: {result.get('score', 'N/A')}")
                    st.write("---")
        else:
            st.error("Invalid Stack Overflow results format")

# Display conversation history at the top
with history_container:
    if len(st.session_state.conversation) > 1:  # More than just the latest response
        st.write("### Previous Conversations")
        for turn in reversed(st.session_state.conversation[:-1]):
            st.write(f"**User Query:** {turn['user']}")
            st.code(turn['response'], language="python")
            st.write("---")
