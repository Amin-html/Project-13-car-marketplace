from fastapi import WebSocket

class AuctionManager:
    def __init__(self):
        self.rooms: dict[int, list[WebSocket]] = {}

    def add(self, listing_id: int, websocket: WebSocket):
        self.rooms.setdefault(listing_id, []).append(websocket)

    def remove(self, listing_id: int, websocket: WebSocket):
        if listing_id in self.rooms:
            self.rooms[listing_id].remove(websocket)
            if not self.rooms[listing_id]:
                del self.rooms[listing_id]

    async def broadcast_local(self, listing_id: int, message: dict):
        for connection in self.rooms.get(listing_id, []):
            await connection.send_json(message)

auction_manager = AuctionManager()