from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # listing_id -> список активных подключений в этой "комнате"
        self.rooms: dict[int, list[WebSocket]] = {}

    async def connect(self, listing_id: int, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(listing_id, []).append(websocket)

    def disconnect(self, listing_id: int, websocket: WebSocket):
        if listing_id in self.rooms:
            self.rooms[listing_id].remove(websocket)
            if not self.rooms[listing_id]:
                del self.rooms[listing_id]

    async def broadcast(self, listing_id: int, message: dict):
        for connection in self.rooms.get(listing_id, []):
            await connection.send_json(message)

chat_manager = ConnectionManager()