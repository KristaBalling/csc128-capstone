
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



    # Classify each new request independently.
    detected_intent = classify_intent(prompt)
    st.session_state.current_intent = detected_intent

    # Preserve collected academic details.
    st.session_state.entities = update_entities(
        st.session_state.entities,
        prompt
    )

    # Official policies and grade appeals require human guidance.
    question = prompt.lower()

    needs_human = (
        "appeal" in question
        or "change my grade" in question
        or (
            "policy" in question
            and any(
                term in question
                for term in (
                    "official", "school", "college",
                    "course", "grade"
                )
            )
        )
    )

    if needs_human:
        response = (
            "I can help you understand the situation, but I "
            "cannot change grades or verify your college's "
            "official policies. Please contact your instructor "
            "or academic advisor and consult your college's "
            "official grade-appeal procedures for accurate "
            "requirements and deadlines. If you provide the "
            "policy text, I can help explain it or help you "
            "draft a respectful message."
        )
    else:
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


