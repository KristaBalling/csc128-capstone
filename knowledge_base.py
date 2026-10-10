
import re

# Academic guidance documents used for grounded responses.
# These are general guidance notes, not official college policies.
DOCUMENTS = {
    "assignment_guidance": """
    Understanding an assignment:
    Read the instructions carefully and identify the required
    deliverables, formatting rules, evaluation criteria, and
    submission deadline. Review the rubric before beginning.
    Break the assignment into smaller tasks and create a
    checklist. Ask the instructor to clarify ambiguous
    requirements rather than making assumptions.
    """,

    "academic_planning": """
    Academic planning:
    Identify all assignments and their deadlines. Estimate
    the time each task requires and prioritize based on
    urgency, complexity, and importance. Divide large
    projects into milestones. Schedule time for research,
    drafting, testing, revision, and submission. Include
    extra time for unexpected problems.
    """,

    "concept_explanation": """
    Learning academic concepts:
    Begin with a clear definition. Explain the concept using
    accessible language and a practical example. Connect
    unfamiliar ideas to concepts the student already knows.
    Encourage active recall, practice problems, and
    explaining the concept in the student's own words.
    """,

    "research_preparation": """
    Preparing for academic research:
    Start with a focused research question. Identify useful
    keywords and search reputable academic databases.
    Evaluate sources for credibility, relevance, evidence,
    and publication date. Distinguish scholarly publications
    from opinion pieces. Record citation information while
    researching. Never invent citations or research findings.
    """
}


def retrieve_documents(query, intent, max_results=2):
    """Retrieve relevant academic guidance passages."""
    query_words = set(
        re.findall(r"[a-zA-Z]{3,}", query.lower())
    )

    results = []

    for category, content in DOCUMENTS.items():
        document_words = set(
            re.findall(r"[a-zA-Z]{3,}", content.lower())
        )

        overlap = len(query_words & document_words)

        # Give the classified intent priority.
        if category == intent:
            overlap += 5

        if overlap > 0:
            results.append((overlap, category, content.strip()))

    results.sort(key=lambda result: result[0], reverse=True)

    return [
        {"category": category, "content": content}
        for _, category, content in results[:max_results]
    ]
