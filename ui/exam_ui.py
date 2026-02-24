# ui/exam_ui.py
import streamlit as st
import time
from core.exam_engine import generate_question
from learning.exam_tracker import record_attempt, get_priority_grammar, get_priority_vocabulary

SECTIONS = ["grammar", "vocabulary", "reading", "listening"]
JLPT_LEVELS = ["N5", "N4", "N3", "N2", "N1"]
TOTAL_QUESTIONS = 60  # Default session length


def render_exam():
    st.sidebar.title("JLPT Exam Mode")

    # ----------------------------
    # Initialize session state
    # ----------------------------
    if "exam_active" not in st.session_state:
        st.session_state.exam_active = False
        st.session_state.current_question = None
        st.session_state.level = "N5"
        st.session_state.section = "grammar"
        st.session_state.selected_answer = None
        st.session_state.pause = False
        st.session_state.current_index = 0
        st.session_state.total_questions = TOTAL_QUESTIONS
        st.session_state.start_time = None
        st.session_state.await_next = False  # Wait for Next Question

    # ----------------------------
    # Sidebar Controls
    # ----------------------------
    st.session_state.level = st.sidebar.selectbox("JLPT Level", JLPT_LEVELS, index=0)
    st.session_state.section = st.sidebar.selectbox("Section", SECTIONS, index=0)

    start_btn, pause_btn, stop_btn = st.sidebar.columns(3)

    with start_btn:
        if st.button("Start Exam"):
            st.session_state.exam_active = True
            st.session_state.pause = False
            st.session_state.current_index = 1
            st.session_state.start_time = time.time()
            st.session_state.current_question = generate_new_question()
            st.session_state.selected_answer = None
            st.session_state.await_next = False

    with pause_btn:
        if st.button("Pause Exam"):
            st.session_state.pause = True

    with stop_btn:
        if st.button("Stop Exam"):
            st.session_state.exam_active = False
            st.session_state.current_question = None
            st.session_state.pause = False
            st.session_state.await_next = False
            st.success("Exam session ended.")

    # ----------------------------
    # Show Timer & Progress
    # ----------------------------
    if st.session_state.exam_active:
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            st.info(f"⏱ Time Elapsed: {minutes:02}:{seconds:02}")

        progress = st.session_state.current_index / st.session_state.total_questions
        st.progress(progress)

    # ----------------------------
    # Display Current Question
    # ----------------------------
    if st.session_state.exam_active and st.session_state.current_question:
        if st.session_state.pause:
            st.info("Exam paused. Resume to continue.")
            if st.button("Resume Exam"):
             st.session_state.pause = False
        else:
            if not st.session_state.await_next:
                display_question(st.session_state.current_question)


# -----------------------------
# Helper functions
# -----------------------------
def generate_new_question():
    """
    Generate a new JLPT-style question using adaptive weakness priority.
    """
    priority = None
    section = st.session_state.section
    level = st.session_state.level

    if section == "grammar":
        priority = get_priority_grammar(level)
    elif section == "vocabulary":
        priority = get_priority_vocabulary(level)

    question = generate_question(
        level=level,
        section=section,
        priority_target=priority
    )
    return question


def display_question(question_data):
    question_num = st.session_state.current_index
    total = st.session_state.total_questions
    st.markdown(f"#### Question {question_num} / {total}")
    st.markdown(f"### {question_data['question']}")
    options = question_data["choices"]

    # Initialize session state for this question
    if f"selected_answer_{question_num}" not in st.session_state:
        st.session_state[f"selected_answer_{question_num}"] = None
    if f"submitted_{question_num}" not in st.session_state:
        st.session_state[f"submitted_{question_num}"] = False

    # Radio button
    st.session_state[f"selected_answer_{question_num}"] = st.radio(
        "Select your answer:",
        options,
        key=f"mcq_radio_{question_num}"
    )
    selected_answer = st.session_state[f"selected_answer_{question_num}"]
    submitted = st.session_state[f"submitted_{question_num}"]

    # ----------------------------
    # Submit Answer Button
    # ----------------------------
    submit_key = f"submit_{question_num}"
    if not submitted and selected_answer is not None:
        if st.button("Submit Answer", key=submit_key):
            correct_index = question_data["answer_index"]
            selected_index = options.index(selected_answer)
            correct = selected_index == correct_index

            # Feedback
            if correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. Correct answer: {options[correct_index]}")

            # Record attempt
            record_attempt(question_data, correct, st.session_state.level)

            # Mark as submitted
            st.session_state[f"submitted_{question_num}"] = True

    # ----------------------------
    # Next Question Button
    # ----------------------------
    next_key = f"next_{question_num}"
    if submitted:
        if st.button("Next Question", key=next_key):
            # Clear state for previous question
            del st.session_state[f"selected_answer_{question_num}"]
            del st.session_state[f"submitted_{question_num}"]

            if st.session_state.current_index < st.session_state.total_questions:
                st.session_state.current_index += 1
                st.session_state.current_question = generate_new_question()
            else:
                st.success("🎉 Exam complete!")
                st.session_state.exam_active = False
                st.session_state.current_question = None