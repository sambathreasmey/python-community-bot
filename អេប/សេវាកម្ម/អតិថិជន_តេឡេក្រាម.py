import logging
from typing import Any

import httpx

from អេប.ស្នូល.កំណត់រចនាសម្ព័ន្ធ import កំណត់

កាត់ត្រា_លុក = logging.getLogger("bot.telegram_client")

អាសយដ្ឋាន_តេឡេក្រាម_ដើម = "https://api.telegram.org"


class អតិថិជនតេឡេក្រាម:
    def __init__(self, តូខិន: str) -> None:
        self._អតិថិជន = httpx.AsyncClient(
            base_url=f"{អាសយដ្ឋាន_តេឡេក្រាម_ដើម}/bot{តូខិន}",
            timeout=10.0,
        )

    async def បិទ(self) -> None:
        await self._អតិថិជន.aclose()

    # ------------------------------------------------------------------
    # ការរៀបចំ Webhook
    # ------------------------------------------------------------------

    async def កំណត់_វេបហ៊ុក(self, អាសយដ្ឋាន: str, តូខិន_សម្ងាត់: str) -> dict:
        ចម្លើយ = await self._អតិថិជន.post(
            "/setWebhook",
            json={
                "url": អាសយដ្ឋាន,
                "secret_token": តូខិន_សម្ងាត់,
                "drop_pending_updates": True,
                "allowed_updates": ["message", "callback_query"],
            },
        )
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def លុប_វេបហ៊ុក(self, លុប_ការបច្ចុប្បន្នភាព_ដែលនៅរង់ចាំ: bool = False) -> dict:
        ចម្លើយ = await self._អតិថិជន.post(
            "/deleteWebhook",
            json={"drop_pending_updates": លុប_ការបច្ចុប្បន្នភាព_ដែលនៅរង់ចាំ},
        )
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def យក_ព័ត៌មាន_វេបហ៊ុក(self) -> dict:
        ចម្លើយ = await self._អតិថិជន.get("/getWebhookInfo")
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    # ------------------------------------------------------------------
    # ការផ្ញើសារ
    # ------------------------------------------------------------------

    async def ផ្ញើសារ(
        self,
        អាយឌី_ឆាត: int,
        អត្ថបទ: str,
        ម៉ាកអាប់: dict | None = None,
        ទម្រង់_អត្ថបទ: str | None = None,
        **ប៉ារ៉ាម៉ែត្របន្ថែម: Any,
    ) -> dict:
        ទិន្នន័យ: dict = {"chat_id": អាយឌី_ឆាត, "text": អត្ថបទ, **ប៉ារ៉ាម៉ែត្របន្ថែម}
        if ម៉ាកអាប់ is not None:
            ទិន្នន័យ["reply_markup"] = ម៉ាកអាប់
        if ទម្រង់_អត្ថបទ is not None:
            ទិន្នន័យ["parse_mode"] = ទម្រង់_អត្ថបទ

        ចម្លើយ = await self._អតិថិជន.post("/sendMessage", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def បញ្ជូនសារបន្ត(
        self, អាយឌី_ឆាត: int, អាយឌី_ឆាត_ដើម: int, អាយឌី_សារ: int, **ប៉ារ៉ាម៉ែត្របន្ថែម: Any
    ) -> dict:
        ទិន្នន័យ: dict = {
            "chat_id": អាយឌី_ឆាត,
            "from_chat_id": អាយឌី_ឆាត_ដើម,
            "message_id": អាយឌី_សារ,
            **ប៉ារ៉ាម៉ែត្របន្ថែម,
        }
        ចម្លើយ = await self._អតិថិជន.post("/forwardMessage", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def ផ្ញើរូបភាព(
        self,
        អាយឌី_ឆាត: int,
        រូបភាព: str,
        ចំណងជើង_រូប: str | None = None,
        ម៉ាកអាប់: dict | None = None,
        **ប៉ារ៉ាម៉ែត្របន្ថែម: Any,
    ) -> dict:
        ទិន្នន័យ: dict = {"chat_id": អាយឌី_ឆាត, "photo": រូបភាព, **ប៉ារ៉ាម៉ែត្របន្ថែម}
        if ចំណងជើង_រូប is not None:
            ទិន្នន័យ["caption"] = ចំណងជើង_រូប
        if ម៉ាកអាប់ is not None:
            ទិន្នន័យ["reply_markup"] = ម៉ាកអាប់

        ចម្លើយ = await self._អតិថិជន.post("/sendPhoto", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def ផ្ញើឯកសារ(
        self,
        អាយឌី_ឆាត: int,
        ឯកសារ: str,
        ចំណងជើង_ឯកសារ: str | None = None,
        ម៉ាកអាប់: dict | None = None,
        **ប៉ារ៉ាម៉ែត្របន្ថែម: Any,
    ) -> dict:
        ទិន្នន័យ: dict = {"chat_id": អាយឌី_ឆាត, "document": ឯកសារ, **ប៉ារ៉ាម៉ែត្របន្ថែម}
        if ចំណងជើង_ឯកសារ is not None:
            ទិន្នន័យ["caption"] = ចំណងជើង_ឯកសារ
        if ម៉ាកអាប់ is not None:
            ទិន្នន័យ["reply_markup"] = ម៉ាកអាប់

        ចម្លើយ = await self._អតិថិជន.post("/sendDocument", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    # ------------------------------------------------------------------
    # ការកែប្រែ / លុបសារ
    # ------------------------------------------------------------------

    async def កែប្រែ_អត្ថបទ_សារ(
        self,
        អាយឌី_ឆាត: int,
        អាយឌី_សារ: int,
        អត្ថបទ: str,
        ម៉ាកអាប់: dict | None = None,
        ទម្រង់_អត្ថបទ: str | None = None,
        **ប៉ារ៉ាម៉ែត្របន្ថែម: Any,
    ) -> dict:
        ទិន្នន័យ: dict = {
            "chat_id": អាយឌី_ឆាត,
            "message_id": អាយឌី_សារ,
            "text": អត្ថបទ,
            **ប៉ារ៉ាម៉ែត្របន្ថែម,
        }
        if ម៉ាកអាប់ is not None:
            ទិន្នន័យ["reply_markup"] = ម៉ាកអាប់
        if ទម្រង់_អត្ថបទ is not None:
            ទិន្នន័យ["parse_mode"] = ទម្រង់_អត្ថបទ

        ចម្លើយ = await self._អតិថិជន.post("/editMessageText", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def កែប្រែ_ម៉ាកអាប់_សារ(
        self, អាយឌី_ឆាត: int, អាយឌី_សារ: int, ម៉ាកអាប់: dict | None = None
    ) -> dict:
        ទិន្នន័យ: dict = {"chat_id": អាយឌី_ឆាត, "message_id": អាយឌី_សារ}
        if ម៉ាកអាប់ is not None:
            ទិន្នន័យ["reply_markup"] = ម៉ាកអាប់

        ចម្លើយ = await self._អតិថិជន.post("/editMessageReplyMarkup", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    async def លុប_សារ(self, អាយឌី_ឆាត: int, អាយឌី_សារ: int) -> dict:
        ចម្លើយ = await self._អតិថិជន.post(
            "/deleteMessage", json={"chat_id": អាយឌី_ឆាត, "message_id": អាយឌី_សារ}
        )
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    # ------------------------------------------------------------------
    # ការឆ្លើយតប Callback Query
    # ------------------------------------------------------------------

    async def ឆ្លើយតប_ខលប៊ែក_ឃ្វើរី(
        self,
        អាយឌី_ខលប៊ែក: str,
        អត្ថបទ: str | None = None,
        បង្ហាញ_ការជូនដំណឹង: bool = False,
    ) -> dict:
        ទិន្នន័យ: dict = {
            "callback_query_id": អាយឌី_ខលប៊ែក,
            "show_alert": បង្ហាញ_ការជូនដំណឹង,
        }
        if អត្ថបទ is not None:
            ទិន្នន័យ["text"] = អត្ថបទ

        ចម្លើយ = await self._អតិថិជន.post("/answerCallbackQuery", json=ទិន្នន័យ)
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()

    # ------------------------------------------------------------------
    # ទាញយកឯកសារ
    # ------------------------------------------------------------------

    async def យក_ឯកសារ(self, អាយឌី_ឯកសារ: str) -> dict:
        ចម្លើយ = await self._អតិថិជន.get("/getFile", params={"file_id": អាយឌី_ឯកសារ})
        ចម្លើយ.raise_for_status()
        return ចម្លើយ.json()


អតិថិជន_តេឡេក្រាម = អតិថិជនតេឡេក្រាម(កំណត់.ថូខិន_តេឡេក្រាម_បត)


# ----------------------------------------------------------------------
# Function ជំនួយសម្រាប់ហៅប្រើប្រាស់ផ្ទាល់
# ----------------------------------------------------------------------


async def ផ្ញើសារ(
    អាយឌី_ឆាត: int, អត្ថបទ: str, ម៉ាកអាប់: dict | None = None, **ប៉ារ៉ាម៉ែត្របន្ថែម: Any
) -> dict:
    return await អតិថិជន_តេឡេក្រាម.ផ្ញើសារ(អាយឌី_ឆាត, អត្ថបទ, ម៉ាកអាប់=ម៉ាកអាប់, **ប៉ារ៉ាម៉ែត្របន្ថែម)


async def កែប្រែ_អត្ថបទ_សារ(
    អាយឌី_ឆាត: int,
    អាយឌី_សារ: int,
    អត្ថបទ: str,
    ម៉ាកអាប់: dict | None = None,
    **ប៉ារ៉ាម៉ែត្របន្ថែម: Any,
) -> dict:
    return await អតិថិជន_តេឡេក្រាម.កែប្រែ_អត្ថបទ_សារ(
        អាយឌី_ឆាត, អាយឌី_សារ, អត្ថបទ, ម៉ាកអាប់=ម៉ាកអាប់, **ប៉ារ៉ាម៉ែត្របន្ថែម
    )


async def លុប_សារ(អាយឌី_ឆាត: int, អាយឌី_សារ: int) -> dict:
    return await អតិថិជន_តេឡេក្រាម.លុប_សារ(អាយឌី_ឆាត, អាយឌី_សារ)


async def ឆ្លើយតប_ខលប៊ែក_ឃ្វើរី(
    អាយឌី_ខលប៊ែក: str, អត្ថបទ: str | None = None, បង្ហាញ_ការជូនដំណឹង: bool = False
) -> dict:
    return await អតិថិជន_តេឡេក្រាម.ឆ្លើយតប_ខលប៊ែក_ឃ្វើរី(
        អាយឌី_ខលប៊ែក, អត្ថបទ=អត្ថបទ, បង្ហាញ_ការជូនដំណឹង=បង្ហាញ_ការជូនដំណឹង
    )