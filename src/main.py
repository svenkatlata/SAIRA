"""Main Module"""

import json
import streamlit as st
from PIL import Image
from chat import get_chat_responses, initialise_converstation
from openalex import initialise_requirements_dictionary

# Load the image correctly
saira_img = Image.open("../public/saira.png")


# Streamlit UI
st.set_page_config(
    page_title="SAIRA | Smart AI Research Assistant",
    page_icon=saira_img,
    initial_sidebar_state="expanded",
)


cols = st.columns([1, 5])
with cols[0]:
    st.image(saira_img, width=100)
with cols[1]:
    st.title("Hey, I am S:red[AI]RA")
    st.write("A Smart AI Research Assistant to Enhance Your Path to New Discoveries.")

# Initiate chat history
if "messages" not in st.session_state:
    st.session_state.messages = initialise_converstation()
    with open("user_requirements.json", "w", encoding="utf-8") as fs:
        json.dump(initialise_requirements_dictionary(), fs)


# Load history on reruns
for message in st.session_state.messages:
    if message.get("role") in ("user", "assistant"):
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("What can I help you with?"):
    # Display user message
    with st.chat_message(name="user"):
        st.write(prompt)

    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get assistant's response and update messages
    st.session_state.messages = get_chat_responses(st.session_state.messages)

    # Display assistant message
    with st.chat_message(name="assistant"):
        assistant_message = st.session_state.messages[-1]["content"]
        st.write(assistant_message)
