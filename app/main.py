import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, status

from app.ai.chat_bot import MODEL_PATH, load_index
from app.api.telegram import router as telegram_router
from app.core.config import settings
from app.services.telegram_client import telegram_client

logger = logging.getLogger("bot.telegram_client")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.path.exists(MODEL_PATH):
        app.state.chatbot_index = load_index()
        logger.info("Loaded existing chatbot_index.pkl")
    webhook_url = f"{settings.PUBLIC_BASE_URL.rstrip('/')}/telegram/webhook"
    await telegram_client.set_webhook(webhook_url, settings.TELEGRAM_WEBHOOK_SECRET)
    yield
    await telegram_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Accounting Helper Service",
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        openapi_url=None if settings.ENVIRONMENT == "production" else "/openapi.json",
        lifespan=lifespan,
    )

    app.include_router(telegram_router)

    @app.get("/healthz", status_code=status.HTTP_200_OK, tags=["System"])
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()
