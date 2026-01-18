import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from deepagents import create_deep_agent
from config.settings import config
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger("streamlit_app")

st.set_page_config(
    page_title=config.get("app_name", "Deep Agent"), page_icon="🤖", layout="wide"
)

st.title("🤖 Deep Agent Experiment")

# --- Utility Functions ---


def get_search_tool():
    """Create and return the Tavily search tool"""
    return TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        # API key is automatically read from TAVILY_API_KEY env var by this tool
    )


# --- Sidebar Configuration ---
st.sidebar.header("Configuration")

# Model options including the one user requested
model_options = [
    "groq:llama-3.3-70b-versatile",
    "groq:qwen/qwen-2.5-coder-32b",
    "groq:qwen/qwen-2.5-32b",
    "groq:llama3-70b-8192",
    "groq:mixtral-8x7b-32768",
    "openai:gpt-4o",
    "openai:gpt-3.5-turbo",
]

selected_model = st.sidebar.selectbox("Select Model", model_options, index=0)
st.sidebar.info(f"App Version: {config.get('version', '0.1.0')}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Status")
if os.getenv("GROQ_API_KEY"):
    st.sidebar.success("GROQ_API_KEY detected")
else:
    st.sidebar.warning("GROQ_API_KEY missing")

if os.getenv("TAVILY_API_KEY"):
    st.sidebar.success("TAVILY_API_KEY detected")
else:
    st.sidebar.warning("TAVILY_API_KEY missing")

# --- Main Interface ---
st.write("Welcome to the Deep Agent experimental playground.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input area
user_input = st.chat_input("Enter your query:")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner(f"Agent is thinking using {selected_model}..."):
            try:
                # 1. Initialize Model
                # Note: 'groq:...' prefix works if langchain-groq is installed and recognized by init_chat_model
                llm = init_chat_model(selected_model)

                # 2. Create Deep Agent
                search_tool = get_search_tool()
                agent = create_deep_agent(
                    model=llm,
                    tools=[search_tool],
                    system_prompt=(
                        "You are a helpful and capable research assistant. "
                        "Use the search tool when necessary to get current information."
                    ),
                )

                # 3. Invoke Agent
                # Passing the conversation history + new message could be better,
                # but currently just passing the new prompt to allow the agent to process it.
                # deep-agent invoke structure:
                payload = {"messages": [{"role": "user", "content": user_input}]}

                result = agent.invoke(payload)

                # 4. Extract and show response
                # Assuming the last message is the final answer
                if "messages" in result and len(result["messages"]) > 0:
                    response_content = result["messages"][-1].content
                else:
                    response_content = "No response generated."

                st.write(response_content)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_content}
                )

            except Exception as e:
                logger.error(f"Error running agent: {e}", exc_info=True)
                st.error(f"An error occurred: {str(e)}")
