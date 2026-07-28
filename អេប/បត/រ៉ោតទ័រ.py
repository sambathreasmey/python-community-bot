import logging

from អេប.បត.អ្នកដោះស្រាយ.លំនាំដើម_អ្នកដោះស្រាយ import សារ_លំនាំដើម_អ្នកដោះស្រាយ

កាត់ត្រា_លុក = logging.getLogger("bot.router")

import httpx


async def handle_update(update: dict) -> None:
    try:
        
        message = update.get("message")
        if not message:
            return

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        await សារ_លំនាំដើម_អ្នកដោះស្រាយ(chat_id, text)
    except httpx.HTTPError:
        កាត់ត្រា_លុក.exception(
            "Unhandled error processing update %s", update.get("update_id")
        )
