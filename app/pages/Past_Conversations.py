import streamlit as st

from app.pages.base import BasePage
from app.pages.utils import ConversationMixins
from app.services.structures.conversation import ConversationList


class PreviousConversationPage(BasePage, ConversationMixins):
    _title = "Previous Conversation"

    def __init__(self, title, session, **kwargs):
        super().__init__(title, session, **kwargs)
        self.file_uploaded = False
        self.file = None
        self.model = None
        self.conversations: ConversationList = ConversationList()

    def _display(self, **kwargs):
        rerun = True
        st.header("Previous Conversation")
        st.write(f"This is the existing conversation page. Continue chatting with your document.")
        return rerun
