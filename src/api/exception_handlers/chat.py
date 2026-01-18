from urllib.request import Request

from fastapi.responses import JSONResponse

from src.core.exceptions.chat import ChatNotFoundError


async def chat_not_found_exception_handler(
    request: Request,
    exc: ChatNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Chat not found",
        },
    )
