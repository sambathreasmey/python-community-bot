import asyncio

from app.ai.chat_bot import get_response
from app.services.telegram_client import telegram_client
from app.utils.otp import generate_otp
from app.utils.payroll import build_payroll_message

BOT_USERNAME = "python_community_chat_bot"


async def handle_default_message(
    chat_id: int, message_id: int, text: str, request
) -> None:

    if text == "/start":
        await telegram_client.send_message(chat_id, "👋 សួស្ដី! កូនBot អ្នកគ្រូសុខេង។")
        return
    if text == "/otp":
        otp = generate_otp()
        await telegram_client.send_message(
            chat_id, f"Your OTP is : <code>{otp}</code>", parse_mode="HTML"
        )
        return
    command = text.split(maxsplit=1)[0] if text else ""
    if command in ("/payroll", f"/payroll@{BOT_USERNAME}"):
        await telegram_client.send_message(
            chat_id, build_payroll_message(), parse_mode="HTML"
        )
        return

    mention_tag = f"@{BOT_USERNAME}"
    if mention_tag in text:
        cleaned_text = text.replace(mention_tag, "").strip()
        chatbot_index = request.app.state.chatbot_index
        response_text, tag, similarity = get_response(cleaned_text, chatbot_index)
        print(tag, similarity)
        await telegram_client.send_message(chat_id, response_text, parse_mode="HTML")
