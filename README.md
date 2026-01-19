# Апи для управления чатами и сообщениями

- POST /chats/ — создать чат
- POST /chats/{id}/messages/ — отправить сообщение
- GET /chats/{id}?limit=N — получить чат и последние N сообщений (по умолчанию 20, максимум 100)
- DELETE /chats/{id} — удалить чат вместе со всеми сообщениями (каскадно)

## Стек

- FastAPI 
- SQLAlchemy 2.0 Async + asyncpg
- PostgreSQL
- Alembic 
- Docker + docker-compose
- pytest + httpx 

## Запуск

Создать dotenv-файл в корень проекта со следующим содержимым ```.env```:

```text
LOG_LEVEL=INFO

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=chat_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/chat_db
```

Далее выполнить команды:

```bash
docker-compose -f pg.docker-compose.yml up -d
```

```bash
docker-compose -f app.docker-compose.yml up -d
```

## Тесты

```bash
pip install pytest pytest-asyncio
```

```bash
pytest
```
