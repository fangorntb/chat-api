import uvicorn
from fastapi import FastAPI

from src.api import ChatsRoutable
from src.api import chat_not_found_exception_handler
from src.core.exceptions.chat import ChatNotFoundError

APP = FastAPI(title='API чатов и сообщений', version='1.0')
APP.include_router(ChatsRoutable().router, )
APP.add_exception_handler(
    ChatNotFoundError,
    chat_not_found_exception_handler,
)
if __name__ == '__main__':
    uvicorn.run(APP)
