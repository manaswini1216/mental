import streamlit as st
from openai import OpenAI
import base64

# Load API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page configuration
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")

# Sidebar disclaimer
st.sidebar.markdown("""
*Disclaimer:*  
This chatbot is not a substitute for professional mental health care. 
If you're in crisis, please contact your local emergency services or a mental health professional.
""")

# Background image function
@st.cache_data
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Apply background if image exists
try:
    bin_str = get_base64("background.png")
    st.markdown(f"""
        <style>
            .main {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        </style>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Background image not found. Using default background.")

# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Function to generate chatbot response
def generate_response(user_input):
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.conversation_history
        )
        ai_response = response.choices[0].message.content.strip()
        st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm having trouble responding right now. Please try again later."

# Function for affirmations
def generate_affirmation():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Give a short positive affirmation to reduce stress."}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating affirmation: {str(e)}")
        return "You are stronger than you think."

# Function for meditation guide
def generate_meditation_guide():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Write a 3-minute guided meditation for relaxation."}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating meditation guide: {str(e)}")
        return "Close your eyes. Take a deep breath... and relax."

# UI
st.title("🧠 Mental Health Support Chatbot")

# Display conversation
for msg in st.session_state.get('conversation_history', []):
    if msg['role'] == "user":
        with st.chat_message("user"):
            st.write(msg['content'])
    else:
        with st.chat_message("assistant"):
            st.write(msg['content'])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_response(prompt)
            st.write(reply)

# Buttons for extra features
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Get Positive Affirmation"):
        with st.spinner("Generating affirmation..."):
            affirmation = generate_affirmation()
            st.info(affirmation)

with col2:
    if st.button("🧘 Get Guided Meditation"):
        with st.spinner("Preparing meditation guide..."):
            meditation = generate_meditation_guide()
            st.success(meditation)

# Clear conversation button
if st.button("🗑 Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
