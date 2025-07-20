import streamlit as st
import google.generativeai as genai
import base64

# Load Gemini API key (store it in Streamlit secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

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

# Apply background
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

# Conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Function to generate chatbot response
def generate_response(user_input):
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    try:
        conversation = [msg["content"] for msg in st.session_state.conversation_history if msg["role"] == "user"]
        combined_input = "\n".join(conversation)
        response = model.generate_content(combined_input)
        ai_response = response.text.strip()
        st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm having trouble responding right now. Please try again later."

# Functions for affirmation and meditation
def generate_affirmation():
    response = model.generate_content("Give a short, positive affirmation for stress relief.")
    return response.text.strip()

def generate_meditation_guide():
    response = model.generate_content("Write a short 3-minute guided meditation for relaxation.")
    return response.text.strip()

# Streamlit UI
st.title("🧠 Mental Health Support Chatbot")

for msg in st.session_state.get('conversation_history', []):
    if msg['role'] == "user":
        with st.chat_message("user"):
            st.write(msg['content'])
    else:
        with st.chat_message("assistant"):
            st.write(msg['content'])

if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_response(prompt)
            st.write(reply)

col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Get Positive Affirmation"):
        with st.spinner("Generating affirmation..."):
            st.info(generate_affirmation())

with col2:
    if st.button("🧘 Get Guided Meditation"):
        with st.spinner("Generating meditation guide..."):
            st.success(generate_meditation_guide())

if st.button("🗑 Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
