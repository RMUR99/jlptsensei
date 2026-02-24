# ui/dashboard.py
import streamlit as st
from learning.vocab_tracker import load_vocab
from learning.grammar_analyzer import load_grammar
from learning.exam_tracker import load_exam_history
import pandas as pd


def dashboard_page():
    st.title("📊 Learning Dashboard")

    # ----------------------------
    # Load data
    # ----------------------------
    vocab_data = load_vocab()
    grammar_data = load_grammar()
    exam_data = load_exam_history(limit=200)  # optional

    words = vocab_data.get("words", [])
    issues = grammar_data.get("issues", {})

    # ----------------------------
    # Metrics
    # ----------------------------
    col_metrics = st.columns(3)
    col_metrics[0].metric("Vocabulary Learned", len(words))
    col_metrics[1].metric("Grammar Points Tracked", len(issues))
    col_metrics[2].metric("Total Exam Attempts", len(exam_data) if exam_data else 0)

    # ----------------------------
    # Two-column layout
    # ----------------------------
    col1, col2 = st.columns(2)

    # ----------------------------
    # Vocabulary Panel
    # ----------------------------
    with col1:
        st.subheader("📚 Vocabulary Learned")
        if words:
            vocab_html = "<div style='height: 400px; overflow-y: auto; border: 1px solid #444; padding: 10px; border-radius: 5px;'>"
            for word in words:
                vocab_html += f"<p style='margin:4px 0;'>{word['word']} ({word.get('reading','')}) - {word.get('meaning','')} [Seen: {word.get('times_seen',0)}]</p>"
            vocab_html += "</div>"
            st.markdown(vocab_html, unsafe_allow_html=True)
        else:
            st.info("No vocabulary learned yet.")

    # ----------------------------
    # Grammar Panel
    # ----------------------------
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

    # ----------------------------
    # Exam Panel
    # ----------------------------
    if not exam_data:
        st.info("No exam attempts recorded yet.")
        return

    df = pd.DataFrame(exam_data)

    # Group per exam session
    grouped = df.groupby("timestamp").agg(
        total_questions=("correct", "count"),
        total_correct=("correct", "sum"),
        level=("level", "first"),
        section=("section", "first")
    ).reset_index()

    # Sort oldest → newest
    grouped = grouped.sort_values("timestamp").reset_index(drop=True)

    # Create Attempt number
    grouped["Attempt"] = grouped.index + 1

    # Create clean X-axis label
    grouped["Label"] = grouped.apply(
        lambda row: f"Attempt {row['Attempt']} ({row['level']})",
        axis=1
    )

    # ---------------------------
    # BAR CHART
    # ---------------------------
    st.subheader("📈 Total Correct per Exam")
    st.bar_chart(
        grouped.set_index("Label")["total_correct"]
    )

    # ---------------------------
    # TABLE SUMMARY
    # ---------------------------
    st.subheader("📋 Exam Summary")
    st.dataframe(
        grouped[["Attempt", "level", "section", "total_correct", "total_questions"]]
    )