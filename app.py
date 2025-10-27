import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key="AIzaSyARxmmZrKotXlNa8BHAV_gunu2C83qr6K0")

# Page configuration
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 5px solid #4CAF50;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .message-content {
        line-height: 1.6;
    }
    .timestamp {
        font-size: 0.75rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    h1 {
        color: #1a237e;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #2196F3;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #1976D2;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-2.5-flash')

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# Sidebar
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=100)
    st.title("⚙️ Settings")
    
    # Model selection
    model_option = st.selectbox(
        "Select Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"],
        help="Choose the Gemini model for your chat"
    )
    
    # Update model if changed
    if "current_model" not in st.session_state:
        st.session_state.current_model = "gemini-2.5-flash"
    
    if model_option != st.session_state.current_model:
        st.session_state.current_model = model_option
        st.session_state.model = genai.GenerativeModel(model_option)
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        st.success(f"✅ Switched to {model_option}")
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: Lower values make responses more focused and deterministic"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "Max Response Length",
        min_value=100,
        max_value=2048,
        value=1024,
        step=100,
        help="Maximum length of the response"
    )
    
    st.divider()
    
    # Chat statistics
    st.subheader("📊 Chat Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("User Messages", len([m for m in st.session_state.messages if m["role"] == "user"]))
    st.metric("AI Responses", len([m for m in st.session_state.messages if m["role"] == "assistant"]))
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    
    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Gemini AI Chatbot**
        
        This is a professional chatbot powered by Google's Gemini AI.
        
        **Features:**
        - Real-time AI responses
        - Conversation history
        - Customizable parameters
        - Professional UI/UX
        
        **Version:** 1.0.0
        """)

# Main chat interface
st.title("🤖 Gemini AI Chatbot")
st.markdown("### Your Intelligent Assistant")

# Display welcome message if no messages
if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! I'm your AI assistant powered by Google Gemini. Ask me anything!")

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">
                👤 You
            </div>
            <div class="message-content">{content}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-header">
                🤖 Gemini AI
            </div>
            <div class="message-content">{content}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...", key="user_input")

if user_input:
    # Get current timestamp
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": current_time
    })
    
    # Display user message immediately
    st.markdown(f"""
    <div class="chat-message user-message">
        <div class="message-header">
            👤 You
        </div>
        <div class="message-content">{user_input}</div>
        <div class="timestamp">{current_time}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show thinking indicator
    with st.spinner("🤔 Thinking..."):
        try:
            # Generate response
            response = st.session_state.chat.send_message(
                user_input,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            assistant_response = response.text
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            
            # Rerun to display the new message
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Powered by Google Gemini AI | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
