
from groq import Groq, RateLimitError, APIError
import streamlit as st
import time
from knowledge_base import retrieve_documents


SYSTEM_PROMPT = """
You are Student Academic Assistant, an AI chatbot
designed to help college students.

You support four primary activities:
1. Understanding assignment instructions.
2. Organizing assignments and study schedules.
3. Explaining academic and technical concepts.
4. Preparing for academic research.

Rules:
- Clearly explain concepts in student-friendly language.
- Help students plan and understand their coursework.
- Ask questions when essential information is missing.
- Do not invent assignment requirements or deadlines.
- Never fabricate research sources or citations.
- Do not complete graded assignments dishonestly.
- Refer official policy questions and grading disputes
  to the student's instructor or academic advisor.
- Do not request student IDs or sensitive personal data.
- Never claim to be a human.
- Keep responses helpful, concise, and encouraging.
"""


def generate_response(messages, intent, entities):
    """Generate an academic response with safe API handling."""

    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)

    except (KeyError, FileNotFoundError):
        return (
            "The AI service is not configured. "
            "Please contact the application administrator."
        )


    # Retrieve relevant academic guidance before calling the model.
    latest_question = messages[-1]["content"] if messages else ""

    documents = retrieve_documents(
        latest_question,
        intent
    )

    retrieved_context = "\n\n".join(
        document["content"] for document in documents
    )

    context = (
        f"Current intent: {intent}\n"
        f"Known assignment details: {entities}\n\n"
        f"Retrieved academic guidance:\n{retrieved_context}\n\n"
        "Use the retrieved guidance when it is relevant. "
        "Treat it as general academic advice, not official school policy. "
        "Do not invent facts, deadlines, or sources. "
        "If information is missing, ask the student for clarification."
    )


    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + "\n" + context
        }
    ]

    # Send recent conversation history to preserve context.
    api_messages.extend(messages[-10:])

    for attempt in range(3):
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=api_messages,
                temperature=0.3,
                max_tokens=400
            )

            return (
                completion.choices[0].message.content
                or "I couldn't generate an answer. Please try again."
            )

        except RateLimitError:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue

            return (
                "I'm receiving too many requests right now. "
                "Please try again in a minute."
            )


        except APIError as error:
            print(f"Groq API error: {type(error).__name__}: {error}")
            return (
                "I can't reach my AI service right now. "
                "Please try again later or contact your instructor."
            )


        except Exception:
            return (
                "Something went wrong while processing your request. "
                "Please try again."
            )
