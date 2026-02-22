import streamlit as st
from learning.vocab_tracker import load_vocab
from learning.grammar_analyzer import load_grammar

def dashboard_page():
    st.title("📊 Learning Dashboard")

    vocab_data = load_vocab()
    grammar_data = load_grammar()

    words = vocab_data.get("words", [])
    issues = grammar_data.get("issues", {})

    st.metric("Vocabulary Learned", len(words))

    col1, col2 = st.columns(2)

    # Build Vocabulary HTML content all at once
    with col1:
        st.subheader("📚 Vocabulary")
        if words:
            vocab_html = "<div style='height: 400px; overflow-y: auto; border: 1px solid #444; padding: 10px; border-radius: 5px;'>"
            for word in words:
                vocab_html += f"<p style='margin:4px 0;'>{word['word']} ({word.get('reading','')}) - {word.get('meaning','')} [Seen: {word.get('times_seen',0)}]</p>"
            vocab_html += "</div>"
            st.markdown(vocab_html, unsafe_allow_html=True)
        else:
            st.info("No vocabulary learned yet.")

    # Build Grammar HTML content all at once
    with col2:
        st.subheader("🧠 Grammar Weaknesses")
        if issues:
            sorted_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)
            grammar_html = "<div style='height: 400px; overflow-y: auto; border: 1px solid #444; padding: 10px; border-radius: 5px;'>"
            for grammar, score in sorted_issues:
                grammar_html += f"<p style='margin:4px 0;'>{grammar} — Weakness: {score}</p>"
            grammar_html += "</div>"
            st.markdown(grammar_html, unsafe_allow_html=True)
        else:
            st.info("No grammar mistakes recorded yet.")