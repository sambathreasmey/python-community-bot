import logging

from app.bot.handlers.default_handler import handle_default_message

logger = logging.getLogger("bot.router")


async def handle_update(update: dict) -> None:
    try:
        
        message = update.get("message")
        if not message:
            return

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        await handle_default_message(chat_id, text)
    except Exception:
        logger.exception(
            "Unhandled error processing update %s", update.get("update_id")
        )
