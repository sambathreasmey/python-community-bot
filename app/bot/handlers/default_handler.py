from app.services.telegram_client import telegram_client
from app.utils.otp import generate_otp

async def handle_default_message(chat_id: int, text: str) -> None:
    if text == "/start":
        await telegram_client.send_message(
            chat_id,
            "👋 Welcome! b b"
        )
        return
    if text == "/otp":
        otp = generate_otp()
        await telegram_client.send_message(
            chat_id,
            f'Your OTP is : <pre>{otp}</pre>',
            parse_mode="HTML"
        )
        return
