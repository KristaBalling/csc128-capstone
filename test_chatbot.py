
from intents import classify_intent
from entities import extract_entities, update_entities
from knowledge_base import retrieve_documents


# Test all four chatbot intents.
def test_assignment_guidance():
    assert classify_intent(
        "Help me understand the assignment rubric"
    ) == "assignment_guidance"


def test_academic_planning():
    assert classify_intent(
        "Help me organize my study schedule"
    ) == "academic_planning"


def test_concept_explanation():
    assert classify_intent(
        "Explain what machine learning means"
    ) == "concept_explanation"


def test_research_preparation():
    assert classify_intent(
        "Help me choose a research topic"
    ) == "research_preparation"


def test_unknown_intent():
    assert classify_intent("") == "unknown"


# Test extraction of multiple academic entities.
def test_entity_extraction():
    result = extract_entities(
        "My Python project is due Friday"
    )

    assert result["assignment_type"] == "project"
    assert result["subject"] == "python"
    assert result["due_date"] == "friday"


# Test memory across conversation turns.
def test_entity_memory():
    current = {
        "assignment_type": None,
        "subject": None,
        "due_date": None
    }

    current = update_entities(
        current, "I have a biology project"
    )
    current = update_entities(
        current, "It is due Monday"
    )

    assert current["assignment_type"] == "project"
    assert current["subject"] == "biology"
    assert current["due_date"] == "monday"


# Test document retrieval.
def test_research_retrieval():
    results = retrieve_documents(
        "How do I evaluate research sources?",
        "research_preparation"
    )

    assert len(results) > 0
    assert results[0]["category"] == "research_preparation"


def test_planning_retrieval():
    results = retrieve_documents(
        "Help me organize my study schedule",
        "academic_planning"
    )

    assert len(results) > 0
    assert results[0]["category"] == "academic_planning"


# Verify an empty query with no intent returns no documents.
def test_empty_retrieval():
    results = retrieve_documents("", "unknown")
    assert results == []
