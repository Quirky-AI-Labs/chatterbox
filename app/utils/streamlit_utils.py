from typing import Generic, Optional, TypeVar

import streamlit as st
from loguru import logger
from pydantic import BaseModel, Field, model_validator
from pydantic.generics import GenericModel

T = TypeVar("T")


class SessionState(GenericModel):
    session: Optional[dict] = Field(..., exclude=False)
    pages: Optional[dict] = Field(default_factory=dict)
    file_uploaded: bool = False
    theme: str = "light"
    user: str = "Random User"
    metadata: Optional[dict] = Field(default_factory=dict)
    vector_store: Optional[T] = Field(default_factory=lambda: None)

    def reset(self):
        self.file_uploaded = False
        self.theme = "light"
        self.user = "Random User"
        self.sync_to_session()

    def to_dict(self):
        return self.model_dump()

    def sync_to_session(self):
        """Sync the values from the SessionState model to st.session_state."""
        for key, value in self.to_dict().items():
            if key == "session":
                continue
            self.session[key] = value

    def sync_from_session(self):
        """Sync the values from st.session_state to the SessionState model."""
        for key in self.__fields__:
            if key == "session":
                continue
            if key in self.session:
                super().__setattr__(key, self.session[key])

    def log_session(self):
        logger.debug(f"Session: {self.session}")

    @model_validator(mode="after")
    def set_session_value(cls, values):
        if not isinstance(values.session, dict):
            values.session = {}
        for value in values:
            if value[0] == "session":
                continue
            values.session[value[0]] = value[1]
        return values

    def __setattr__(self, name, value):
        if name == "session" and self.session is not None:
            raise AttributeError("Session cannot be set directly")
        super().__setattr__(name, value)
        if name != "session" and self.session is not None:
            self.session[name] = value

    class Config:
        arbitrary_types_allowed = True
