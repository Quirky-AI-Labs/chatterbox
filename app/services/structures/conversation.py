from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class Message(BaseModel):
    id: str = Field(alias="_id", default_factory=lambda: str(uuid4()))
    sender: str
    message: str
    created_at: str = Field(default_factory=lambda: str(datetime.now()))

    def __str__(self):
        return f"Message()"

    def __repr__(self):
        return f"Message()"


class Conversation(BaseModel):
    id: str = Field(alias="_id", default_factory=lambda: str(uuid4()))
    query: Message
    response: Message
    context: Optional[str] = None
    created_at: str = Field(default_factory=lambda: str(datetime.now()))

    def __str__(self):
        return f"Conversation()"

    def __repr__(self):
        return f"Conversation()"

    def __len__(self):
        return len(self.conversations)


class ConversationList(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: Optional[str] = Field(default="Conversation - Chatterbox 101")
    conversations: List[Conversation] = list()
    context_files: List[str] = list()
    created_at: str = Field(default_factory=lambda: str(datetime.now()))

    def add_conversation(self, conversation: Conversation):
        self.conversations.append(conversation)

    def __len__(self):
        return len(self.conversations)

    def __getitem__(self, index):
        return self.conversations[index]

    def __iter__(self):
        return iter(self.conversations)

    def __repr__(self):
        return f"ConversationList()"

    def __str__(self):
        return f"ConversationList()"

    @model_validator(mode="after")
    def add_default_conversation(cls, values):
        DEFAULT_MESSAGE = [
            Conversation(
                query=Message(
                    sender="User",
                    message="I am a software developer who is trying to build a chatbot. Can you help me?",
                ),
                response=Message(sender="Bot", message="Hi, I am Chatterbox 101. How can I help you?"),
            )
        ]
        if len(values.conversations) == 0:
            values.conversations = DEFAULT_MESSAGE
        return values
