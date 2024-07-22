import streamlit as st

from app.pages.base import BasePage


class PreviousConversationPage(BasePage):
    _title = "Previous Conversation"

    def _display(self, **kwargs):
        rerun = True
        st.header("Previous Conversation")
        st.write(f"This is the existing conversation page. Continue chatting with your document.")
        return rerun
