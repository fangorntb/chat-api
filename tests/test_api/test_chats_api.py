import pytest


@pytest.mark.asyncio
async def test_create_chat(client):
    response = await client.post(
        "/chats/",
        json={"title": "Test chat"},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Test chat"


@pytest.mark.asyncio
async def test_send_message(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "Hello"},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["chat_id"] == chat_id
    assert data["text"] == "Hello"


@pytest.mark.asyncio
async def test_send_message_chat_not_found(client):
    response = await client.post(
        "/chats/999/messages/",
        json={"text": "Fail"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_get_chat_with_messages(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    for i in range(5):
        await client.post(
            f"/chats/{chat_id}/messages/",
            json={"text": f"msg-{i}"},
        )

    response = await client.get(f"/chats/{chat_id}?limit=3")

    assert response.status_code == 200

    data = response.json()
    assert data["chat"]["id"] == chat_id
    assert len(data["messages"]) == 3


@pytest.mark.asyncio
async def test_get_chat_limit_max(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    for i in range(150):
        await client.post(
            f"/chats/{chat_id}/messages/",
            json={"text": str(i)},
        )

    response = await client.get(f"/chats/{chat_id}?limit=200")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_chat_cascade(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "msg"},
    )

    delete_resp = await client.delete(f"/chats/{chat_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/chats/{chat_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_chat_not_found(client):
    response = await client.delete("/chats/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_chat_empty_title(client):
    response = await client.post(
        "/chats/",
        json={"title": ""},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_chat_title_only_spaces(client):
    response = await client.post(
        "/chats/",
        json={"title": "   "},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_chat_title_too_long(client):
    response = await client.post(
        "/chats/",
        json={"title": "a" * 201},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_chat_title_trimmed(client):
    response = await client.post(
        "/chats/",
        json={"title": "   Мой чат   "},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Мой чат"


@pytest.mark.asyncio
async def test_send_message_empty_text(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": ""},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_message_text_only_spaces(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "     "},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_message_text_too_long(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "a" * 5001},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_message_text_trimmed(client):
    chat = await client.post("/chats/", json={"title": "Chat"})
    chat_id = chat.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "  Hello world  "},
    )

    assert response.status_code == 201

    assert response.json()["text"] == "Hello world"
