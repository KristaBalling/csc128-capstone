
# Student Academic Assistant

CSC-128 Chatbot Programming I — Capstone Project

## Overview

Student Academic Assistant is an AI-powered chatbot designed to help college students understand assignments, organize coursework, learn academic concepts, and prepare for research.

Built with Python, Streamlit, and the Groq API.

## Features

The chatbot supports four primary intents:

1. **Assignment Guidance** — Explains instructions, rubrics, and assignment requirements.
2. **Academic Planning** — Helps organize assignments, deadlines, and study schedules.
3. **Concept Explanation** — Explains academic and technical concepts.
4. **Research Preparation** — Helps formulate research questions and evaluate sources.

Additional capabilities include:

- Intent classification using deterministic Python logic
- Entity extraction for assignment types, subjects, and deadlines
- Conversation memory using Streamlit session state
- AI-generated responses through Groq
- Retrieval from a small academic guidance knowledge base
- Graceful handling of API failures and rate limits
- AI disclosure and academic integrity boundaries

## Project Structure

- `app.py` — Streamlit interface and conversation management
- `intents.py` — Intent classification
- `entities.py` — Entity extraction and memory updates
- `knowledge_base.py` — Academic guidance retrieval
- `ai_service.py` — Groq integration and error handling
- `test_chatbot.py` — Automated tests
- `requirements.txt` — Pinned application dependencies
- `.gitignore` — Excludes secrets and local files

## Installation

Clone the repository and install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` containing:

```toml
GROQ_API_KEY = "your_api_key_here"
```

Never commit API keys to GitHub.

## Running the Application

```bash
python -m streamlit run app.py
```

## Testing

Install pytest:

```bash
python -m pip install pytest
```

Run the automated tests:

```bash
python -m pytest test_chatbot.py -v
```

## Responsible AI

This chatbot identifies itself as AI software, avoids fabricating sources and academic requirements, and refers official policy or grading questions to appropriate college staff.

It provides general academic support rather than official institutional guidance.

## Limitations

- The knowledge base contains general academic guidance, not official college policies.
- Conversation memory persists only during the current Streamlit session.
- AI-generated responses should be reviewed for accuracy.
- The application requires a working Groq API connection.

## Deployment

The application is designed for deployment on Streamlit Community Cloud using a public GitHub repository. The Groq API key must be configured separately in the deployed application's Secrets settings.
