from fastapi import Depends, Query, status
from classy_fastapi import Routable, get, post, delete

from src.api.schemas import (
    ChatCreateRequest,
    ChatResponse,
    ChatWithMessagesResponse,
    MessageCreateRequest,
    MessageResponse,
)
from src.core.services.chat import ChatService
from src.api.dependencies import get_chat_service


class ChatsRoutable(Routable):

    @post(
        "/chats/",
        response_model=ChatResponse,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_chat(
        self,
        payload: ChatCreateRequest,
        service: ChatService = Depends(get_chat_service),
    ):
        return await service.create_chat(payload.title)

    @post(
        "/chats/{id}/messages/",
        response_model=MessageResponse,
        status_code=status.HTTP_201_CREATED,
        responses={
            404: {"description": "Chat not found"},
        },
    )
    async def send_message(
        self,
        id: int,
        payload: MessageCreateRequest,
        service: ChatService = Depends(get_chat_service),
    ):
        return await service.send_message(id, payload.text)

    @get(
        "/chats/{id}",
        response_model=ChatWithMessagesResponse,
        responses={
            404: {"description": "Chat not found"},
        },
    )
    async def get_chat(
        self,
        id: int,
        limit: int = Query(default=20, ge=1, le=100),
        service: ChatService = Depends(get_chat_service),
    ):
        chat, messages = await service.get_chat_with_messages(id, limit)
        return ChatWithMessagesResponse(chat=chat, messages=messages)

    @delete(
        "/chats/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            404: {"description": "Chat not found"},
        },
    )
    async def delete_chat(
        self,
        id: int,
        service: ChatService = Depends(get_chat_service),
    ):
        await service.delete_chat(id)
        return None
