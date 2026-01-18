import uvicorn
from fastapi import FastAPI

from src.api import ChatsRoutable

APP = FastAPI(title='Апи для создания чатов')
APP.include_router(ChatsRoutable().router, )

if __name__ == '__main__':
    uvicorn.run(APP)
