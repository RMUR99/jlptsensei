import streamlit as st
from ui.chat_ui import chat_page
from ui.dashboard import dashboard_page


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Chat", "Dashboard"]
)

if page == "Chat":
    chat_page()

elif page == "Dashboard":
    dashboard_page()
