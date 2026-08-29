import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from asgiref.sync import sync_to_async
from app.core.security import verify_token
from app.core.pubsub import redis_client, auction_channel, publish_bid
from app.ws.auction_manager import auction_manager

router = APIRouter()

async def redis_listener(listing_id: int):
    """Слушает Redis Pub/Sub канал этого listing и рассылает всем локальным подключениям этого процесса."""
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(auction_channel(listing_id))
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = json.loads(message["data"])
            await auction_manager.broadcast_local(listing_id, data)
    finally:
        await pubsub.unsubscribe(auction_channel(listing_id))


@router.websocket("/ws/auction/{listing_id}")
async def auction_room(websocket: WebSocket, listing_id: int, token: str = Query(...)):
    payload = verify_token(token)
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = int(payload["sub"])

    await websocket.accept()
    auction_manager.add(listing_id, websocket)

    listener_task = asyncio.create_task(redis_listener(listing_id))

    try:
        while True:
            data = await websocket.receive_json()
            amount = data.get("amount")
            if not amount:
                continue

            from auctions.models import Bid

            def place_bid():
                top = Bid.objects.filter(listing_id=listing_id).order_by("-amount").first()
                if top and float(amount) <= float(top.amount):
                    return None  # ставка не выше текущей топ-ставки
                return Bid.objects.create(listing_id=listing_id, bidder_id=user_id, amount=amount)

            bid = await sync_to_async(place_bid)()
            if bid is None:
                await websocket.send_json({"type": "error", "detail": "Bid too low"})
                continue

            await publish_bid(listing_id, {
                "type": "new_top_bid",
                "bidder_id": user_id,
                "amount": str(bid.amount),
                "created_at": bid.created_at.isoformat(),
            })
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        auction_manager.remove(listing_id, websocket)
        listener_task.cancel()