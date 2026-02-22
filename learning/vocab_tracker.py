import json
import os
import streamlit as st
VOCAB_PATH = os.path.join("data", "vocabulary.json")
os.makedirs("data", exist_ok=True)

def load_vocab():
    if not os.path.exists(VOCAB_PATH) or os.path.getsize(VOCAB_PATH) == 0:
        return {"words": []}
    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vocab(data):
    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_vocab(new_words):
    data = load_vocab()
    if "words" not in data:
        data["words"] = []

    word_map = {w["word"]: w for w in data["words"]}

    for word in new_words:
        w = word_map.get(word["word"])
        if w:
            w["times_seen"] += 1
        else:
            new_entry = {
                "word": word["word"],
                "reading": word.get("reading",""),
                "meaning": word.get("meaning",""),
                "times_seen": 1,
                "times_predicted": 0
            }
            data["words"].append(new_entry)
            word_map[word["word"]] = new_entry
            #st.write("Added to vocab:", new_entry)  # Debug

    save_vocab(data)
    #st.write("Saved data to:", VOCAB_PATH)
    #st.write("Current vocab:", data)