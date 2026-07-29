import asyncio

import emoji

from app.services.telegram_client import telegram_client
from app.utils.otp import generate_otp


async def handle_default_message(chat_id: int, message_id: int, text: str) -> None:

    # Check for emojis
    if emoji.emoji_count(text) > 0:
        asyncio.create_task(
            telegram_client.delete_message_with_countdown(
                chat_id, message_id, seconds=5
            )
        )
        return

    if text == "/start":
        await telegram_client.send_message(chat_id, "👋 សួស្ដី! កូនBot អ្នកគ្រូសុខេង។")
        return
    if text == "/otp":
        otp = generate_otp()
        await telegram_client.send_message(
            chat_id, f"Your OTP is : <code>{otp}</code>", parse_mode="HTML"
        )
        return
