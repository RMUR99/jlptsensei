from difflib import SequenceMatcher
import re
import jaconv


def normalize_text(text):
 
    text = jaconv.kata2hira(text)
    text = jaconv.z2h(text, kana=False, ascii=True, digit=True)
    # Remove whitespace
    text = re.sub(r"\s+", "", text)
    return text


def similarity_score(original, spoken):
    original_clean = normalize_text(original)
    spoken_clean = normalize_text(spoken)
    ratio = SequenceMatcher(None, original_clean, spoken_clean).ratio()
    return round(ratio * 100, 2)