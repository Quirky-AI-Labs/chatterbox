import streamlit as st

from app.services.structures.conversation import Conversation


class ConversationMixins:
    def display_conversation_list(self):
        for conversation in self.conversations:
            self._display_conversation(conversation)

    # @st.cache_data
    def _display_conversation(self, conversation: Conversation):
        query = conversation.query
        response = conversation.response
        with st.chat_message("user"):
            st.text(query.message)
        with st.chat_message("assistant"):
            st.markdown(response.message)
