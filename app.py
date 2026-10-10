
import streamlit as st
from intents import classify_intent
from entities import update_entities
from ai_service import generate_response

st.set_page_config(
    page_title="Student Academic Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("Student Academic Assistant")

st.caption("An AI-powered chatbot for academic planning and research support.")

st.info(
    "You are interacting with an AI assistant, not a human. "
    "Always verify official course requirements with your instructor."
)

st.write("Welcome! I can help you with:")
st.markdown("""
- Understanding assignment instructions
- Organizing coursework and deadlines
- Explaining academic concepts
- Preparing for academic research
""")


# Store the conversation across Streamlit reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []


# Remember academic details throughout the conversation.
if "entities" not in st.session_state:
    st.session_state.entities = {
        "assignment_type": None,
        "subject": None,
        "due_date": None
    }

if "current_intent" not in st.session_state:
    st.session_state.current_intent = None


# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept and display a new message.
if prompt := st.chat_input("What can I help you with today?"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)


    # Identify the student's request.
    detected_intent = classify_intent(prompt)

    if detected_intent != "unknown":
        st.session_state.current_intent = detected_intent

    # Collect new details without forgetting earlier ones.
    st.session_state.entities = update_entities(
        st.session_state.entities,
        prompt
    )

    # Generate a response using the student's intent and saved details.
    with st.spinner("Thinking..."):
        response = generate_response(
            st.session_state.messages,
            st.session_state.current_intent,
            st.session_state.entities
        )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Temporary diagnostic panel for testing.
    with st.expander("Debug: Chatbot Memory"):
        st.write("Current intent:", st.session_state.current_intent)
        st.write("Collected entities:", st.session_state.entities)


