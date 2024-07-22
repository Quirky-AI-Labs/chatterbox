from typing import List

import streamlit as st
from loguru import logger

# from pages import BasePage, HomePage, NewConversationPage, PreviousConversationPage
from app.pages.base import BasePage
from app.pages.Home_Page import HomePage
from app.pages.New_Conversation import NewConversationPage
from app.pages.Past_Conversations import PreviousConversationPage
from app.utils.streamlit_utils import SessionState


def initialize_session():
    session = SessionState(session=st.session_state)
    return session


def main():
    session = initialize_session()
    pages: List[BasePage] = {
        "Home": HomePage("Home", session),
        "New Conversation": NewConversationPage("New Conversation", session),
        "Previous Conversations": PreviousConversationPage("Previous Conversations", session),
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page: BasePage = pages[selection]
    page.display()


if __name__ == "__main__":
    main()
