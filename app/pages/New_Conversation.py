import streamlit as st

from app.pages.base import BasePage


class NewConversationPage(BasePage):
    _title = "New Conversation"

    def _display(self, **kwargs):
        rerun = True
        st.header("New Conversation")
        st.write(f"This is the new conversation page. Upload your document for chatting with it.")
        return rerun
