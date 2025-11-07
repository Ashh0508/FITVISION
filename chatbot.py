import os
from dotenv import load_dotenv
import streamlit as st
from typing import Literal
# from langchain_community.chat_models import ChatOpenAI # --- CHANGE: Commented out OpenAI
from langchain_groq import ChatGroq # --- CHANGE: Imported Groq
from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationSummaryMemory # --- CHANGE: Using BufferWindowMemory for simplicity with Groq
from langchain.chains.conversation.memory import ConversationBufferWindowMemory # --- CHANGE: Using BufferWindowMemory
from dataclasses import dataclass
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)


# Load environment variables from .env file
load_dotenv()

@dataclass
class Message:
    origin: Literal["human", "ai"]
    message: str

def initialize_session_state():
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "history" not in st.session_state:
        st.session_state.history = []
    if "conversation" not in st.session_state:
        groq_api_key = os.getenv("GROQ_API_KEY") # --- CHANGE: Using GROQ_API_KEY

        if not groq_api_key:
            st.error("GROQ_API_KEY environment variable not found. Please add it to your .env file.")
            st.stop() # Stop execution if key is missing

        llm = ChatGroq( # --- CHANGE: Using ChatGroq
            temperature=0.7, # Groq recommends temp between 0.0 and 1.0
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile" # --- CHANGE: Specified Groq model
        )

        # --- CHANGE: Using ConversationBufferWindowMemory as SummaryMemory requires more complex setup ---
        # It keeps the last 'k' interactions
        conversation_memory = ConversationBufferWindowMemory(k=5, return_messages=True) 

        # Insert prompt as knowledge base to the chatbot to behave as an AI personal Trainer
        # --- Adjusted initial context saving for BufferWindowMemory ---
        # We'll use a standard prompt template instead of saving initial context this way.

        # --- Define the prompt structure ---
        system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are a chatbot inserted in a web app that uses AI to classify and count the repetitions of home exercises. Act as an expert in fitness and respond to the user as their personal AI trainer. Answer the user's questions truthfully based on general fitness knowledge.""")
        human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
        prompt_template = ChatPromptTemplate.from_messages([
            system_msg_template, 
            MessagesPlaceholder(variable_name="history"), # Placeholder for memory
            human_msg_template
        ])

        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=conversation_memory,
            prompt=prompt_template, # --- Added prompt template ---
            verbose=True # Shows more detailed logs in the console
        )

def on_click_callback():
    human_prompt = st.session_state.get('human_prompt', '')
    if human_prompt:
        try:
            with st.spinner("Thinking..."): # Added spinner for user feedback
                 llm_response = st.session_state.conversation.run(human_prompt)

            st.session_state.history.append(Message("human", human_prompt))
            st.session_state.history.append(Message("ai", llm_response))
            st.session_state.token_count += len(llm_response.split()) # Example token approximation

            # Clear the text input field after submitting the message
            st.session_state.human_prompt = ""
        except Exception as e:
            st.error(f"Error getting response from Groq: {e}")


def chat_ui():
    initialize_session_state()
    st.title("Ask me anything about Fitness 🤖")

    # Define custom CSS style for message
    custom_css = """
        <style>
            .chat-bubble {
                background-color: #f1f0f0;
                padding: 10px 15px;
                border-radius: 20px;
                margin-bottom: 10px;
                max-width: 70%;
                display: inline-block;
                word-wrap: break-word; /* Wrap long words */
                color: black; /* Set text color to black */
            }
            .chat-row {
                 display: flex;
                 margin-bottom: 10px;
            }
           .row-reverse {
                 justify-content: flex-end;
            }
            .user-bubble {
                background-color: #d0f0f0;
                /* align-self: flex-end; */ /* Handled by row-reverse */
                /* margin-left: auto; */ /* Let flexbox handle alignment */
                color: black; /* Set text color to black */
            }
            .ai-bubble {
                background-color: #f0f0f0;
                 /* align-self: flex-start; */ /* Default behavior */
                color: black; /* Set text color to black */
            }
        </style>
    """

    # Display custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")

    with chat_placeholder:
        for chat in st.session_state.history:
            div = f"""
            <div class="chat-row {'row-reverse' if chat.origin == 'human' else ''}">
                <div class="chat-bubble {'user-bubble' if chat.origin == 'human' else 'ai-bubble'}">
                    {chat.message}
                </div>
            </div>
            """
            st.markdown(div, unsafe_allow_html=True)

    with prompt_placeholder:
        st.text_input("Chat", key="human_prompt", placeholder="Ask your fitness question...") # Added placeholder
        st.form_submit_button("Submit", on_click=on_click_callback)

    # st.caption(f"Used {st.session_state.token_count} tokens") # Optional: Display token count

if __name__ == "__main__":
    chat_ui()
