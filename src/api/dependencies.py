from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.chat import ChatService
from src.infrastructure.db.session_maker import get_session


def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    return ChatService(session)
