from fastapi import Depends, HTTPException, Query, status
from classy_fastapi import Routable, get, post, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session_maker import get_session
from src.db.repositories import ChatRepository, MessageRepository
from src.api.schemas import (
    ChatCreateRequest,
    ChatResponse, ChatWithMessagesResponse,
    MessageCreateRequest,
    MessageResponse,
)


class ChatsRoutable(Routable):

    @post("/chats", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
    async def create_chat(
            self,
            payload: ChatCreateRequest,
            session: AsyncSession = Depends(get_session),
    ):
        """
        Метод создания чата.
        """
        return await ChatRepository(session).create(title=payload.title)

    @post(
        "/chats/{id}/messages/",
        response_model=MessageResponse,
        status_code=status.HTTP_201_CREATED,
        responses={404: {'detail': 'Chat not found'}}
    )
    async def send_message(
            self,
            id: int,
            payload: MessageCreateRequest,
            session: AsyncSession = Depends(get_session),
    ):
        """
        Метод отправки сообщения в чат.
        """
        chat = await ChatRepository(session).get_by_id(id)
        self.handle_chat_not_found(chat)

        return await MessageRepository(session).create(
            chat_id=id,
            text=payload.text,
        )

    @classmethod
    def handle_chat_not_found(cls, chat):
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

    @get("/chats/{id}", response_model=ChatWithMessagesResponse, )
    async def get_chat(
            self,
            id: int,
            limit: int = Query(default=20, ge=1, le=100),
            session: AsyncSession = Depends(get_session),
    ):
        """
        Метод получения чата.
        """
        chat = await ChatRepository(session).get_by_id(id)
        self.handle_chat_not_found(chat)

        messages = await MessageRepository(session).get_last_by_chat(
            chat_id=id,
            limit=limit,
        )

        return ChatWithMessagesResponse(
            chat=chat,
            messages=messages
        )

    @delete(
        "/chats/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={404: {'detail': 'Chat not found'}},
    )
    async def delete_chat(
            self,
            id: int,
            session: AsyncSession = Depends(get_session),
    ):
        """
        Метод удаления чата.
        """
        deleted = await ChatRepository(session).delete_by_id(id)
        self.handle_chat_not_found(deleted)
        return None
