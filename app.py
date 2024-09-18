from typing import List

import streamlit as st
from loguru import logger

from app.pages.base import BasePage
from app.pages.Home_Page import HomePage
from app.pages.New_Conversation import NewConversationPage
from app.pages.Past_Conversations import PreviousConversationPage
from app.utils.streamlit_utils import SessionState


def initialize_session():
    if "session_state" not in st.session_state:
        st.session_state["session_state"] = SessionState(session=st.session_state)
        st.session_state["session_state"].sync_to_session()
    else:
        st.session_state["session_state"].sync_from_session()
    return st.session_state["session_state"]


def main():
    session = initialize_session()
    pages: List[BasePage] = {
        "Home": HomePage("Home", session),
        "New Conversation": NewConversationPage("New Conversation", session),
        "Previous Conversations": PreviousConversationPage("Previous Conversations", session),
    }

    logger.info("========================================")
    logger.info("Starting Chatterbox 101")
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    selection = "New Conversation"
    page: BasePage = pages[selection]
    page.display()


if __name__ == "__main__":
    main()
