from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from asgiref.sync import sync_to_async
from app.core.security import verify_token
from app.ws.connection_manager import chat_manager

router = APIRouter()

@router.websocket("/ws/chat/{listing_id}")
async def chat_room(websocket: WebSocket, listing_id: int, token: str = Query(...)):
    payload = verify_token(token)
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = int(payload["sub"])

    await chat_manager.connect(listing_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "").strip()
            if not content:
                continue

            from chat.models import ChatMessage

            def save_message():
                return ChatMessage.objects.create(
                    listing_id=listing_id, sender_id=user_id, content=content
                )

            message = await sync_to_async(save_message)()

            await chat_manager.broadcast(listing_id, {
                "type": "message",
                "sender_id": user_id,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            })
    except WebSocketDisconnect:
        chat_manager.disconnect(listing_id, websocket)