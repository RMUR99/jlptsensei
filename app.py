import streamlit as st
from ui.chat_ui import chat_page
from ui.dashboard import dashboard_page
from ui.exam_ui import render_exam 

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Chat", "Dashboard", "JLPT Exam"]  
)

if page == "Chat":
    chat_page()

elif page == "Dashboard":
    dashboard_page()

elif page == "JLPT Exam":
    render_exam()  