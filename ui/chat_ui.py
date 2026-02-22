import streamlit as st
from io import BytesIO
import jaconv
import re
from core.llm_engine import generate_reply
from learning.vocab_tracker import update_vocab
from learning.grammar_analyzer import update_grammar
from learning.shadowing import similarity_score
from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from streamlit_mic_recorder import mic_recorder

# ------------------------------
# TTS caching
# ------------------------------
@st.cache_data(show_spinner=False)
def get_audio(text: str) -> bytes:
    return speak(text)

# ------------------------------
# Normalize Japanese text
# ------------------------------
def normalize_japanese(text):
    text = jaconv.kata2hira(text)
    text = jaconv.z2h(text, kana=False, ascii=True, digit=True)
    return re.sub(r"\s+", "", text)

# ------------------------------
# Voice input handler
# ------------------------------
def handle_voice_input(audio_input):
    if isinstance(audio_input, dict):
        audio_bytes = audio_input.get("audio") or audio_input.get("bytes")
    else:
        audio_bytes = audio_input
    if not audio_bytes:
        return None
    return transcribe(BytesIO(audio_bytes) if isinstance(audio_bytes, bytes) else audio_bytes)

# ------------------------------
# Main Chat Page
# ------------------------------
def chat_page():
    st.title("JLPT AI Tutor 日本語能力試験の先生")

    # JLPT Settings
    level = st.selectbox("Choose JLPT Level", ["N5","N4","N3","N2","N1"])
    strict_mode = st.checkbox("Strict JLPT Mode")
    mode = st.selectbox("Mode", ["Conversation", "Shadowing Practice"])

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "shadow_sentence" not in st.session_state:
        st.session_state.shadow_sentence = None

    # ==============================
    # Conversation Mode
    # ==============================
    if mode == "Conversation":
        st.subheader("💬 Conversation Mode")

        # Display chat history
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        user_input = None

        # Voice input
        audio_input = mic_recorder("🎙 Speak", "Stop Recording")
        if audio_input:
            result = handle_voice_input(audio_input)
            if result:
                user_input = result["text"]
                st.chat_message("user").write(user_input)

        # Text input fallback
        text_input = st.chat_input("Type your message in Japanese...")
        if text_input:
            user_input = text_input
            st.chat_message("user").write(user_input)

        # AI reply
        if user_input:
            result = generate_reply(
                st.session_state.messages + [{"role":"user","content":user_input}],
                level,
                strict_mode
            )

            # Ensure result is dict
            if not isinstance(result, dict):
                result = {"reply": str(result), "vocabulary": [], "grammar_points": []}

            reply_text = result.get("reply", "")
            new_vocab = result.get("vocabulary", [])
            grammar_points = result.get("grammar_points", [])

            if reply_text:
                st.session_state.messages.append({"role":"assistant","content":reply_text})
                st.chat_message("assistant").write(reply_text)

                # ----------------------
                # Save vocabulary silently
                # ----------------------
                if isinstance(new_vocab, list) and new_vocab:
                    update_vocab(new_vocab)  # no st.write / debug

                # ----------------------
                # Save grammar safely
                # ----------------------
                all_grammar = []
                if isinstance(grammar_points, list):
                    all_grammar.extend(grammar_points)
                # Include AI-corrected grammar from vocabulary if present
                if isinstance(new_vocab, list):
                    for v in new_vocab:
                        if isinstance(v, dict) and v.get("grammar_issue"):
                            all_grammar.append(v["grammar_issue"])

                safe_grammar = []
                for g in all_grammar:
                    if isinstance(g, dict) and "grammar_issue" in g:
                        safe_grammar.append(g["grammar_issue"])
                    elif isinstance(g, str):
                        safe_grammar.append(g)
                if safe_grammar:
                    update_grammar(safe_grammar)

                # ----------------------
                # Optional clean feedback
                # ----------------------
                with st.expander("📘 Learning Feedback"):
                    if new_vocab:
                        st.write("### Vocabulary")
                        for v in new_vocab:
                            st.write(f"{v['word']} ({v.get('reading','')}) — {v.get('meaning','')}")
                    if safe_grammar:
                        st.write("### Grammar Corrections")
                        for g in safe_grammar:
                            st.write(f"- {g}")

                # ----------------------
                # TTS
                # ----------------------
                try:
                    st.audio(get_audio(reply_text), format="audio/mp3")
                except:
                    pass

    # ==============================
    # Shadowing Mode
    # ==============================
    elif mode == "Shadowing Practice":
        st.subheader("🎤 Shadowing Practice")

        if st.button("Generate JLPT Sentence"):
            result = generate_reply(
                [{"role":"user","content":f"Give one short JLPT {level} sentence for shadowing practice. Max 12 words."}],
                level,
                strict_mode
            )

            full_explanation = result.get("reply","") if isinstance(result, dict) else str(result)
            japanese_sentence_only = full_explanation.split("\n")[0].split("(")[0].strip()

            st.session_state.shadow_sentence = japanese_sentence_only
            st.session_state.shadow_explanation = full_explanation

            st.write(full_explanation)

        if st.session_state.shadow_sentence:
            audio_input = mic_recorder("🎙 Start Speaking", "Stop Recording")
            if audio_input:
                result = handle_voice_input(audio_input)
                if result:
                    spoken_text = result["text"]
                    duration = result["duration"]

                    st.write(f"You said: {spoken_text}")

                    ref_norm = normalize_japanese(st.session_state.shadow_sentence)
                    spoken_norm = normalize_japanese(spoken_text)

                    similarity = round(similarity_score(ref_norm, spoken_norm), 1)
                    char_count = len(spoken_norm)
                    cpm = round((char_count / duration) * 60) if duration > 0 else 0

                    st.metric("Pronunciation Similarity", f"{similarity}%")
                    st.write(f"Speed: {cpm} chars/min")

                    if similarity > 85:
                        st.success("Excellent pronunciation!")
                    elif similarity > 60:
                        st.warning("Good, but improve rhythm.")
                    else:
                        st.error("Try again slowly.")