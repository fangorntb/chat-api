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

```bash
docker-compose -f pg.docker-compose.yml up --build
```

```bash
docker-compose -f app.docker-compose.yml up --build
```