from sqlalchemy import select, desc

from src.infrastructure.db.models import Message
from ._base import AbstractRepository


class MessageRepository(AbstractRepository):

    async def create(self, chat_id: int, text: str) -> Message:
        message = Message(chat_id=chat_id, text=text)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_last_by_chat(
        self,
        chat_id: int,
        limit: int,
    ) -> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at), desc(Message.id))
            .limit(limit)
        )

        messages = list(result.scalars().all())
        messages.reverse()
        return messages
