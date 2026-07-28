import logging

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, status

from អេប.បត.រ៉ោតទ័រ import handle_update
from អេប.ស្នូល.កំណត់រចនាសម្ព័ន្ធ import កំណត់

កាត់ត្រា_លុក = logging.getLogger("telegram.webhook")
រ៉ោតទ័រ = APIRouter(prefix="/telegram", tags=["Telegram"])


@រ៉ោតទ័រ.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if x_telegram_bot_api_secret_token != កំណត់.តេឡេក្រាម_គេហទំព័រ_សម្ងាត់:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret token"
        )

    update = await request.json()

    # Ack Telegram immediately — do real work after the response is sent.
    background_tasks.add_task(handle_update, update)
    return {"ok": True}