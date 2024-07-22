import streamlit as st

from app.pages.base import BasePage


class HomePage(BasePage):
    _title = "Home Page"

    def _display(self, **kwargs):
        rerun = True
        st.header("Home Page")
        st.write(f"This is the home page. Navigate to the Conversations tab to start chatting with your document.")
        return rerun
