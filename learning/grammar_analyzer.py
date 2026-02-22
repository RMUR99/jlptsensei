
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

GRAMMAR_PATH = os.path.join(PROJECT_ROOT, "data", "grammar_issues.json")

def load_grammar():
    if not os.path.exists(GRAMMAR_PATH):
        return {"issues": {}}

    if os.path.getsize(GRAMMAR_PATH) == 0:
        return {"issues": {}}

    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_grammar(data):
    with open(GRAMMAR_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_grammar(mistakes):

    data = load_grammar()

    # Make sure data["issues"] exists
    if "issues" not in data or not isinstance(data["issues"], dict):
        data["issues"] = {}

    for m in mistakes:
        # Handle string or dict
        if isinstance(m, dict) and "grammar_issue" in m:
            issue = m["grammar_issue"]
        elif isinstance(m, str):
            issue = m
        else:
            # skip invalid item
            continue

        # Count occurrences
        if issue in data["issues"]:
            data["issues"][issue] += 1
        else:
            data["issues"][issue] = 1

    save_grammar(data)