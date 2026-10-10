
import re

# Subjects commonly found in college coursework.
SUBJECTS = [
    "python", "programming", "computer science",
    "machine learning", "artificial intelligence",
    "math", "algebra", "statistics", "biology",
    "chemistry", "physics", "history", "english",
    "psychology", "research"
]

ASSIGNMENT_TYPES = [
    "quiz", "test", "exam", "essay", "paper",
    "project", "lab", "discussion", "presentation",
    "homework", "assignment"
]

WEEKDAYS = [
    "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday"
]


def find_match(text, options):
    """Match whole words or phrases, not partial words."""
    for option in sorted(options, key=len, reverse=True):
        if re.search(
            r"\b" + re.escape(option) + r"\b",
            text,
            re.IGNORECASE
        ):
            return option
    return None


def extract_entities(message):
    """Extract academic information from a student's message."""
    text = message.strip()

    assignment_type = find_match(text, ASSIGNMENT_TYPES)
    subject = find_match(text, SUBJECTS)

    weekday = find_match(text, WEEKDAYS)

    # Recognize common numeric date formats.
    date_match = re.search(
        r"\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b",
        text
    )

    due_date = (
        date_match.group(0)
        if date_match
        else weekday
    )

    return {
        "assignment_type": assignment_type,
        "subject": subject,
        "due_date": due_date
    }


def update_entities(current_entities, message):
    """Preserve previously collected information across turns."""
    new_entities = extract_entities(message)

    updated = current_entities.copy()

    for key, value in new_entities.items():
        if value is not None:
            updated[key] = value

    return updated
