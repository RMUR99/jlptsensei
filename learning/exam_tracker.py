
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

EXAM_PATH = os.path.join(PROJECT_ROOT, "data", "exam_tracker.json")


def _initialize_file():
    """Create exam_tracker.json if it doesn't exist or is empty."""
    if not os.path.exists(EXAM_PATH) or os.path.getsize(EXAM_PATH) == 0:
        default_data = {
            "summary": {"total": 0, "correct": 0},
            "by_section": {},
            "by_level": {},
            "weak_grammar": {},
            "weak_vocabulary": {},
            "history": []
        }
        with open(EXAM_PATH, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)

def _load_data():
    _initialize_file()
    with open(EXAM_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data):
    with open(EXAM_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------
# Public API
# ---------------------------------------------------

def record_attempt(question_data: dict, correct: bool, level: str):
    """
    Records a single exam attempt.
    """

    data = _load_data()

    section = question_data["section"]
    grammar_point = question_data.get("grammar_point")
    vocabulary_focus = question_data.get("vocabulary_focus")

    # 1️⃣ Update summary
    data["summary"]["total"] += 1
    if correct:
        data["summary"]["correct"] += 1

    # 2️⃣ Update section stats
    if section not in data["by_section"]:
        data["by_section"][section] = {"total": 0, "correct": 0}

    data["by_section"][section]["total"] += 1
    if correct:
        data["by_section"][section]["correct"] += 1

    # 3️⃣ Update level stats
    if level not in data["by_level"]:
        data["by_level"][level] = {"total": 0, "correct": 0}

    data["by_level"][level]["total"] += 1
    if correct:
        data["by_level"][level]["correct"] += 1

    # 4️⃣ Track weak grammar
    if grammar_point:
        if grammar_point not in data["weak_grammar"]:
            data["weak_grammar"][grammar_point] = {"total": 0, "wrong": 0}

        data["weak_grammar"][grammar_point]["total"] += 1
        if not correct:
            data["weak_grammar"][grammar_point]["wrong"] += 1

    # 5️⃣ Track weak vocabulary
    if vocabulary_focus:
        if vocabulary_focus not in data["weak_vocabulary"]:
            data["weak_vocabulary"][vocabulary_focus] = {"total": 0, "wrong": 0}

        data["weak_vocabulary"][vocabulary_focus]["total"] += 1
        if not correct:
            data["weak_vocabulary"][vocabulary_focus]["wrong"] += 1

    # 6️⃣ Add lightweight history record
    data["history"].append({
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "section": section,
        "correct": correct,
        "grammar_point": grammar_point,
        "vocabulary_focus": vocabulary_focus
    })

    _save_data(data)


# ---------------------------------------------------
# Weakness Retrieval
# ---------------------------------------------------

def get_priority_grammar(level: str, min_attempts=3, threshold=0.5):
    """
    Returns most problematic grammar point.
    """

    data = _load_data()

    worst_point = None
    worst_ratio = 0

    for point, stats in data["weak_grammar"].items():
        total = stats["total"]
        wrong = stats["wrong"]

        if total < min_attempts:
            continue

        ratio = wrong / total

        if ratio > threshold and ratio > worst_ratio:
            worst_ratio = ratio
            worst_point = point

    return worst_point


def get_priority_vocabulary(level: str, min_attempts=3, threshold=0.5):

    
    """
    Returns most problematic vocabulary word.
    """

    data = _load_data()

    worst_word = None
    worst_ratio = 0

    for word, stats in data["weak_vocabulary"].items():
        total = stats["total"]
        wrong = stats["wrong"]

        if total < min_attempts:
            continue

        ratio = wrong / total

        if ratio > threshold and ratio > worst_ratio:
            worst_ratio = ratio
            worst_word = word

    return worst_word


# ---------------------------------------------------
# History Retrieval
# ---------------------------------------------------

def load_exam_history(limit: int | None = None):
    """
    Returns exam attempt history.
    If limit is provided, returns only the most recent 'limit' attempts.
    """
    data = _load_data()
    history = data.get("history", [])

    if limit:
        return history[-limit:]
    return history