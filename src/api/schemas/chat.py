from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from src.api.schemas.message import MessageResponse


class ChatCreateRequest(BaseModel):
    title: str = Field(
        description='Заголовок чата. Не может быть пустым или состоять только из пробельных символов',
        min_length=1,
        max_length=200,
    )

    @field_validator("title")
    @classmethod
    def trim_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title must not be empty")
        return v


class ChatResponse(BaseModel):
    id: int = Field(description='Идентификатор чата')
    title: str = Field(description='Заголовок чата')
    created_at: datetime = Field(description='Датавремя создания чата')

    class Config:
        from_attributes = True


class ChatWithMessagesResponse(BaseModel):
    chat: ChatResponse = Field(description='Объект чата')
    messages: list[MessageResponse] = Field(default_factory=list, description='Последние N-сообщений в чате')

    class Config:
        from_attributes = True
