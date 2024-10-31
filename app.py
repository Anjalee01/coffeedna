import streamlit as st
from backend.chat_logic import get_coffee_recommendation
from backend.chat_history import load_history


import streamlit as st
st.set_page_config(page_title="CoffeeDNA Chat", page_icon="☕", layout="centered")


# User Session State for user_id, input history
if 'user_id' not in st.session_state:
    st.session_state.user_id = "12345"  
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


st.sidebar.title("User Preferences")
language = st.sidebar.selectbox("Language", ["English", "Bahasa Indonesia"])
tone = st.sidebar.selectbox("Tone", ["friendly", "professional"])
detail_level = st.sidebar.selectbox("Detail Level", ["concise", "detailed"])
flavor_profile = st.sidebar.text_input("Flavor Profile", "strong, bold")
bean_type = st.sidebar.text_input("Bean Type", "Arabica")

st.title("☕ CoffeeDNA Chat")
st.markdown("### Discover Your Perfect Coffee Match!")

# Main chat function
def chat():
    user_input = st.text_input("Enter your message here...", key="user_input")

    if st.button("Send"):
        if user_input:
            user_preferences = {
                "language": language,
                "tone": tone,
                "detail_level": detail_level,
                "flavor_profile": flavor_profile,
                "bean_type": bean_type
            }
            response = get_coffee_recommendation(st.session_state.user_id, user_input, user_preferences)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**CoffeeDNA:** {message['content']}")

# Run chat function
chat()
