from abc import ABC, abstractmethod
from typing import Optional

import streamlit as st


class BasePage(ABC):
    def __init__(self, title: str, state: Optional[object] = None, **kwargs):
        self.title = title
        self.state = state
        self.params = kwargs

    @abstractmethod
    def _display(self, **kwargs):
        raise NotImplementedError("Page should have something to display. Implement this method in the child class.")

    def display(self, **kwargs):
        self._display(**kwargs)


class EmptyPage(BasePage):
    def _display(self, **kwargs):
        st.write(f"Empty page: {self.title}")
        return True
