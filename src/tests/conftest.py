import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app import APP
from src.db.models import Base
from src.db.session_maker import get_session

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(init_models())
    yield
    asyncio.run(drop_models())
    asyncio.run(engine.dispose())


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession):
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    APP.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=APP)

    async with AsyncClient(
            transport=transport,
            base_url="http://test",
    ) as ac:
        yield ac

    APP.dependency_overrides.clear()
