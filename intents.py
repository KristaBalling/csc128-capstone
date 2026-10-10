
import re

# Each intent represents a distinct student need.
INTENT_KEYWORDS = {
    "assignment_guidance": [
        "assignment", "instructions", "rubric",
        "requirements", "homework", "project",
        "what do i need to do"
    ],
    "academic_planning": [
        "plan", "schedule", "organize", "deadline",
        "due date", "prioritize", "study plan",
        "time management"
    ],
    "concept_explanation": [
        "explain", "what is", "what does",
        "how does", "definition", "concept",
        "understand", "difference between"
    ],
    "research_preparation": [
        "research", "sources", "topic", "hypothesis",
        "research question", "citation",
        "academic article", "literature review"
    ]
}


def classify_intent(message):
    """Identify the student's primary request using keyword matching."""
    text = message.lower().strip()

    if not text:
        return "unknown"

    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(
            1 for keyword in keywords
            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            )
        )

    # When scores tie, prefer planning for explicit planning requests.
    if scores["academic_planning"] > 0 and re.search(
            r"\b(plan|planning|schedule|organize|prioritize)\b",
            text
    ):
        best_intent = "academic_planning"
    else:
        best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "unknown"

    return best_intent
