import os

import streamlit as st
from loguru import logger

from app.pages.base import BasePage
from app.pages.utils import ConversationMixins
from app.services.ingress.channel import OCRDocument
from app.services.retrievers.retriever import Retriever
from app.services.structures.conversation import Conversation, ConversationList, Message

tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))
os.makedirs(tmp_dir, exist_ok=True)


class NewConversationPage(BasePage, ConversationMixins):
    _title = "New Conversation"

    def save_file(self, file):
        path = os.path.join(tmp_dir, file.name)
        logger.debug(f"Saving file to: {path}")
        with open(path, "wb") as f:
            f.write(file.getvalue())
        return path

    def __init__(self, title, session, **kwargs):
        super().__init__(title, session, **kwargs)
        self.file_uploaded = False
        self.file = None
        self.model = None
        self.retriever = None
        logger.info(f"Session: {session}")
        if session.vector_store is not None:
            self.retriever = Retriever.from_vector_store(session.vector_store)
        last_conversation = list(self.session.pages.keys())
        if last_conversation:
            self.conversations = ConversationList(**self.session.pages[last_conversation[-1]])
        else:
            self.conversations: ConversationList = ConversationList()

    def _display(self, **kwargs):
        rerun = True
        st.header("Starting New Conversation!!!")
        st.write(f"This is the new conversation page. Upload your document for chatting with it.")
        logger.info("Displaying new conversation page.")
        if uploaded_file := st.file_uploader("Choose a file", accept_multiple_files=True):
            logger.info(f"Uploaded file: {uploaded_file} | {type(uploaded_file)}")
            for file in uploaded_file:
                file_path = self.save_file(file)
                if file_path in self.conversations.context_files:
                    st.warning(f"File {file_path} already uploaded.")
                    continue
                self.conversations.context_files.append(file_path)
                self.session.pages[self.conversations.id] = self.conversations.model_dump()
                ocr_document = OCRDocument(file_path)
                documents = ocr_document.generate_document()
                # chunks = ocr_document.get_splitted_docs(documents)
                if self.retriever is None:
                    self.retriever = Retriever.from_documents(documents)
                    self.session.vector_store = self.retriever.vector_store
                else:
                    self.retriever.add_documents(documents)
                    self.session.vector_store = self.retriever.vector_store

        self.display_conversation_list()
        user_input = st.chat_input("Input your question!")
        logger.info(f"User input: {user_input} | {type(user_input)}")
        if user_input:
            conversation = Conversation(
                query=Message(sender="user", message=user_input),
                response=Message(sender="assistant", message="I am a bot!"),
            )
            response = self.retriever.get_response(user_input)
            conversation.response.message = response.get(
                "answer", "No context for the given query found in the document."
            )
            conversation.context = "\n".join([doc.page_content for doc in response["context"]])
            self.conversations.add_conversation(conversation)
            self.session.pages[self.conversations.id] = self.conversations.model_dump()
            self._display_conversation(conversation)
        return rerun
