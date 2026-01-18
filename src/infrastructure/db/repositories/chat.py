from sqlalchemy import select, delete

from src.infrastructure.db.models import Chat
from ._base import AbstractRepository


class ChatRepository(AbstractRepository):
    async def create(self, title: str) -> Chat:
        chat = Chat(title=title)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def get_by_id(self, chat_id: int) -> Chat | None:
        result = await self.session.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, chat_id: int) -> bool:
        result = await self.session.execute(
            delete(Chat)
            .where(Chat.id == chat_id)
            .returning(Chat.id)
        )
        deleted_id = result.scalar_one_or_none()
        await self.session.commit()
        return deleted_id is not None
