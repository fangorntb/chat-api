from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class MessageCreateRequest(BaseModel):
    text: str = Field(
        description='Текст сообщения. '
                    'Не может быть пустым или содержать только пробельные символы.',
        min_length=1,
        max_length=5000,
    )

    @field_validator("text")
    @classmethod
    def trim_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text must not be empty")
        return v


class MessageResponse(BaseModel):
    id: int = Field(description='Идетификатор сообщения')
    chat_id: int = Field(description='ID чата, к которому относится сообщение')
    text: str = Field(description='Текст сообщения')
    created_at: datetime = Field(description='Датавремя создания сообщения')

    class Config:
        from_attributes = True
