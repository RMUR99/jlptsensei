# core/exam_engine.py
from core.llm_engine import generate_exam_question
from core.jlpt_rules import JLPT_RULES
from core.prompt_builder import build_exam_prompt
import hashlib

ALLOWED_SECTIONS = ["grammar", "vocabulary", "reading", "listening"]

def generate_question(level: str, section: str, priority_target: str | None = None):
    """
    Generate one JLPT-style MCQ question with a stable unique ID for session tracking.
    """

    if section not in ALLOWED_SECTIONS:
        raise ValueError(f"Invalid section: {section}")

    constraints = JLPT_RULES[level]

    prompt = build_exam_prompt(
        level=level,
        section=section,
        constraints=constraints,
        priority_target=priority_target
    )

    question_data = generate_exam_question(prompt)

    # 4️⃣ Validate structure
    validated = _validate_question_structure(question_data)

    # 5️⃣ Add a unique question ID (hash of question text + section)
    question_text = validated["question"]
    unique_id = hashlib.md5(f"{section}-{question_text}".encode("utf-8")).hexdigest()
    validated["id"] = unique_id

    return validated


def _validate_question_structure(data: dict):
    """
    Ensure LLM output matches required structure.
    """

    required_keys = [
        "question",
        "choices",
        "answer_index",
        "explanation",
        "section",
        "grammar_point",
        "vocabulary_focus"
    ]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing key in question data: {key}")

    if not isinstance(data["choices"], list) or len(data["choices"]) != 4:
        raise ValueError("MCQ must contain exactly 4 choices.")

    if not isinstance(data["answer_index"], int):
        raise ValueError("answer_index must be integer.")

    if not (0 <= data["answer_index"] <= 3):
        raise ValueError("answer_index must be between 0-3.")

    return data