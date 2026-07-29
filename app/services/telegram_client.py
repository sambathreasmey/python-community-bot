import asyncio
import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger("bot.telegram_client")

# Dictionary to manage state per chat:
# {chat_id: {"msg_id": int | None, "task": asyncio.Task | None}}
_active_warning_tasks: dict[int, dict] = {}

TELEGRAM_API_BASE = "https://api.telegram.org"


class TelegramClient:
    def __init__(self, token: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=f"{TELEGRAM_API_BASE}/bot{token}",
            timeout=10.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Webhook setup
    # ------------------------------------------------------------------

    async def set_webhook(self, url: str, secret_token: str) -> dict:
        response = await self._client.post(
            "/setWebhook",
            json={
                "url": url,
                "secret_token": secret_token,
                "drop_pending_updates": True,
                "allowed_updates": ["message", "callback_query"],
            },
        )
        response.raise_for_status()
        return response.json()

    async def delete_webhook(self, drop_pending_updates: bool = False) -> dict:
        response = await self._client.post(
            "/deleteWebhook",
            json={"drop_pending_updates": drop_pending_updates},
        )
        response.raise_for_status()
        return response.json()

    async def get_webhook_info(self) -> dict:
        response = await self._client.get("/getWebhookInfo")
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Sending messages
    # ------------------------------------------------------------------

    async def send_message(
        self,
        chat_id: int,
        text: str,
        markup: dict | None = None,
        parse_mode: str | None = None,
        **kwargs: Any,
    ) -> dict:
        payload: dict = {"chat_id": chat_id, "text": text, **kwargs}
        if markup is not None:
            payload["reply_markup"] = markup
        if parse_mode is not None:
            payload["parse_mode"] = parse_mode

        response = await self._client.post("/sendMessage", json=payload)
        response.raise_for_status()
        return response.json()

    async def forward_message(
        self, chat_id: int, from_chat_id: int, message_id: int, **kwargs: Any
    ) -> dict:
        """
        Native Telegram forward -- copies the message (with its original
        'Forwarded from' attribution) into `chat_id`, no re-typing needed.
        """
        payload: dict = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            **kwargs,
        }
        response = await self._client.post("/forwardMessage", json=payload)
        response.raise_for_status()
        return response.json()

    async def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str | None = None,
        markup: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        payload: dict = {"chat_id": chat_id, "photo": photo, **kwargs}
        if caption is not None:
            payload["caption"] = caption
        if markup is not None:
            payload["reply_markup"] = markup

        response = await self._client.post("/sendPhoto", json=payload)
        response.raise_for_status()
        return response.json()

    async def send_document(
        self,
        chat_id: int,
        document: str,
        caption: str | None = None,
        markup: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        payload: dict = {"chat_id": chat_id, "document": document, **kwargs}
        if caption is not None:
            payload["caption"] = caption
        if markup is not None:
            payload["reply_markup"] = markup

        response = await self._client.post("/sendDocument", json=payload)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Editing / deleting messages
    # ------------------------------------------------------------------

    async def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        markup: dict | None = None,
        parse_mode: str | None = None,
        **kwargs: Any,
    ) -> dict:
        payload: dict = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            **kwargs,
        }
        if markup is not None:
            payload["reply_markup"] = markup
        if parse_mode is not None:
            payload["parse_mode"] = parse_mode

        response = await self._client.post("/editMessageText", json=payload)
        response.raise_for_status()
        return response.json()

    async def edit_message_reply_markup(
        self, chat_id: int, message_id: int, markup: dict | None = None
    ) -> dict:
        payload: dict = {"chat_id": chat_id, "message_id": message_id}
        if markup is not None:
            payload["reply_markup"] = markup

        response = await self._client.post("/editMessageReplyMarkup", json=payload)
        response.raise_for_status()
        return response.json()

    async def delete_message(self, chat_id: int, message_id: int) -> dict:
        response = await self._client.post(
            "/deleteMessage", json={"chat_id": chat_id, "message_id": message_id}
        )
        response.raise_for_status()
        return response.json()

    async def delete_message_with_countdown(
        self, chat_id: int, user_message_id: int, seconds: int = 5
    ) -> None:
        """Deletes the user's emoji message immediately and manages a debounced warning countdown."""

        # 1. Delete original user's message immediately
        try:
            await self.delete_message(chat_id, user_message_id)
        except httpx.HTTPError as exc:
            logger.warning(
                "Failed to delete original user message %s in chat %s: %s",
                user_message_id,
                chat_id,
                exc,
            )

        # 2. Cancel any running warning task for this chat to avoid spam/rate limits
        if chat_id in _active_warning_tasks and _active_warning_tasks[chat_id].get(
            "task"
        ):
            _active_warning_tasks[chat_id]["task"].cancel()

        # 3. Spawn a new countdown task in background
        task = asyncio.create_task(self._run_warning_countdown(chat_id, seconds))

        existing_msg_id = _active_warning_tasks.get(chat_id, {}).get("msg_id")
        _active_warning_tasks[chat_id] = {
            "msg_id": existing_msg_id,
            "task": task,
        }

    async def _run_warning_countdown(self, chat_id: int, seconds: int) -> None:
        """Internal helper to update or send the warning message and count down."""
        warning_msg_id = _active_warning_tasks.get(chat_id, {}).get("msg_id")

        try:
            # If no active warning exists, send a new one
            if not warning_msg_id:
                warning_msg = await self.send_message(
                    chat_id,
                    f"⚠️ Emojis are not allowed! Deleting warning in <b>{seconds}s</b>...",
                    parse_mode="HTML",
                )
                warning_msg_id = warning_msg["result"]["message_id"]
                _active_warning_tasks[chat_id]["msg_id"] = warning_msg_id
            else:
                # Re-use existing warning message and reset countdown text
                await self.edit_message_text(
                    chat_id,
                    warning_msg_id,
                    f"⚠️ Emojis are not allowed! Deleting warning in <b>{seconds}s</b>...",
                    parse_mode="HTML",
                )

            # Count down second by second
            for remaining in range(seconds - 1, 0, -1):
                await asyncio.sleep(1)
                await self.edit_message_text(
                    chat_id,
                    warning_msg_id,
                    f"⚠️ Emojis are not allowed! Deleting warning in <b>{remaining}s</b>...",
                    parse_mode="HTML",
                )

            await asyncio.sleep(1)

            # Clean up warning message once countdown reaches 0
            await self.delete_message(chat_id, warning_msg_id)

        except asyncio.CancelledError:
            # Task was cancelled because another emoji message arrived; leave the warning message active
            return
        except httpx.HTTPError as exc:
            logger.warning("Error during countdown edit for chat %s: %s", chat_id, exc)
        finally:
            # Clean up global tracking dictionary if this task completed naturally
            current_task = asyncio.current_task()
            if _active_warning_tasks.get(chat_id, {}).get("task") == current_task:
                _active_warning_tasks.pop(chat_id, None)

    # ------------------------------------------------------------------
    # Callback queries
    # ------------------------------------------------------------------

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> dict:
        payload: dict = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert,
        }
        if text is not None:
            payload["text"] = text

        response = await self._client.post("/answerCallbackQuery", json=payload)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Files
    # ------------------------------------------------------------------

    async def get_file(self, file_id: str) -> dict:
        response = await self._client.get("/getFile", params={"file_id": file_id})
        response.raise_for_status()
        return response.json()


telegram_client = TelegramClient(settings.TELEGRAM_BOT_TOKEN)


# ----------------------------------------------------------------------
# Module-level convenience wrappers
# (so handlers can `from app.services.telegram_client import send_message`
# instead of reaching into the `telegram_client` singleton directly)
# ----------------------------------------------------------------------


async def send_message(
    chat_id: int, text: str, markup: dict | None = None, **kwargs: Any
) -> dict:
    return await telegram_client.send_message(chat_id, text, markup=markup, **kwargs)


async def edit_message_text(
    chat_id: int,
    message_id: int,
    text: str,
    markup: dict | None = None,
    **kwargs: Any,
) -> dict:
    return await telegram_client.edit_message_text(
        chat_id, message_id, text, markup=markup, **kwargs
    )


async def delete_message(chat_id: int, message_id: int) -> dict:
    return await telegram_client.delete_message(chat_id, message_id)


async def answer_callback_query(
    callback_query_id: str, text: str | None = None, show_alert: bool = False
) -> dict:
    return await telegram_client.answer_callback_query(
        callback_query_id, text=text, show_alert=show_alert
    )
