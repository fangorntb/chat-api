from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.base import BaseService
from src.infrastructure.db.repositories import ChatRepository, MessageRepository
from src.core.exceptions.chat import ChatNotFoundError


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_repo = ChatRepository(session)
        self.message_repo = MessageRepository(session)

    async def create_chat(self, title: str):
        return await self.chat_repo.create(title=title)

    async def _get_chat_or_fail(self, chat_id: int):
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise ChatNotFoundError()
        return chat

    async def get_chat_with_messages(self, chat_id: int, limit: int):
        chat = await self._get_chat_or_fail(chat_id)
        messages = await self.message_repo.get_last_by_chat(
            chat_id=chat_id,
            limit=limit,
        )
        return chat, messages

    async def send_message(self, chat_id: int, text: str):
        await self._get_chat_or_fail(chat_id)
        return await self.message_repo.create(
            chat_id=chat_id,
            text=text,
        )

    async def delete_chat(self, chat_id: int):
        deleted = await self.chat_repo.delete_by_id(chat_id)
        if not deleted:
            raise ChatNotFoundError()

