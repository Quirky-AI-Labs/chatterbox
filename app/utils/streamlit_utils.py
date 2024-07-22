from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field, model_validator


class SessionState(BaseModel):
    session: Optional[dict] = Field(..., exclude=False)
    file_uploaded: bool = False
    theme: str = "light"
    user: str = "Random User"

    def reset(self):
        self.file_uploaded = False
        self.theme = "light"
        self.user = "Random User"

    def to_dict(self):
        return self.model_dump()

    def to_session(self, session):
        for key, value in self.to_dict().items():
            if key == "session":
                continue
            self.session[key] = value

    def log_session(self):
        logger.debug(f"Session: {self.session}")

    @model_validator(mode="after")
    def set_session_value(cls, values):
        if not isinstance(values.session, dict):
            session_state = {}
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
