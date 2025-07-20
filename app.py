import streamlit as st
import openai
import base64

openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")

st.sidebar.markdown("""
*Disclaimer:*  
This chatbot is not a substitute for professional mental health care. 
If you're in crisis, please contact your local emergency services or a mental health professional.
""")

@st.cache_data
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
            .stChatInput {{
                background-color: rgba(255, 255, 255, 0.8);
            }}
        </style>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Background image not found. Using default background.")

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def generate_response(user_input):
    try:
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=st.session_state.conversation_history,
            temperature=0.7
        )

        ai_response = response['choices'][0]['message']['content']
        st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm having trouble responding right now. Please try again later."

def generate_affirmation():
    try:
        prompt = "Provide a concise, uplifting positive affirmation to encourage someone who is feeling stressed or overwhelmed. Keep it to 1-2 sentences."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        st.error(f"Error generating affirmation: {str(e)}")
        return "You are stronger than you think. Keep going!"

def generate_meditation_guide():
    try:
        prompt = "Provide a brief 3-5 minute guided meditation script to help someone relax and reduce stress. Include breathing instructions and body relaxation guidance."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        st.error(f"Error generating meditation guide: {str(e)}")
        return "Find a comfortable position. Close your eyes. Take a deep breath in... and slowly exhale."

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
            response = generate_response(prompt)
            st.write(response)

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

if st.button("🗑 Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
