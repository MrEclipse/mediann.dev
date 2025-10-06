from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from app.providers import AppProvider
from app.routes import router

"""Создание FastAPI приложения с DI и роутами"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Applications Service", lifespan=lifespan)
    app.include_router(router)
    container = make_async_container(AppProvider())
    setup_dishka(container, app)
    return app


app = create_app()
