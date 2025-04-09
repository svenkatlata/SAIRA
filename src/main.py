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

# Sidebar Title
st.sidebar.title("📚 SAIRA – Smart AI Research Assistant")

st.sidebar.markdown(
    """
    **SAIRA** is an AI-powered research companion designed to help you explore, discover, and ideate across the research landscape.  
    Whether you're conducting literature reviews, exploring new research areas, or just brainstorming ideas — SAIRA is your intelligent hub for:  
    - 🔍 Finding relevant research papers  
    - 💡 Exploring thought experiments  
    - 📖 Understanding existing literature  
    - 📝 Even identifying gaps to publish your own work  
    """
)

# Static Instructions
st.sidebar.markdown("### 🚀 How to Use")
st.sidebar.markdown(
    """
    1. **Start with a clear research topic** – something that already has active research.
    2. **Provide specific links** (e.g., DOI URLs) if you have particular papers or queries in mind.
    3. **Mention preferences** like sorting (e.g., by citations, date) or whether you want only open-access papers.
    4. SAIRA will suggest **keywords** based on your intent. You can customize them if needed.
    5. Once keywords are finalized, SAIRA will list **relevant topics** to choose from.
    6. Select a topic, and SAIRA will fetch a curated list of research papers for you.
    """
)

# Precautions / Limitations
st.sidebar.markdown("### ⚠️ Please Note")
st.sidebar.markdown(
    """
    - **Session-based memory only:** All chat history will be lost once you refresh the browser.
    - **Experimental tool:** This is an early prototype, so it does not support chat saving yet.
    - **One topic per session:** For best results, avoid switching topics in the same chat. Start fresh with a browser refresh.
    """
)

# Developer Info
st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **Developed by:** [Lata Venkat](https://github.com/svenkatlata)")
st.sidebar.markdown(
    """
    💬 Have feedback, found a bug, or just curious about the tool?  
    Feel free to reach out — I'd love to connect!
    """
)
st.sidebar.markdown("✉️ svenkatlata@gmail.com")

# Footer or App Version
st.sidebar.markdown("---")
st.sidebar.markdown("Version: `1.0.0`")

