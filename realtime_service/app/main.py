from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, status
from app.core.security import verify_token

app = FastAPI(title="Car Marketplace Realtime")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws/echo")
async def websocket_echo(websocket: WebSocket, token: str = Query(...)):
    payload = verify_token(token)
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    user_id = payload["sub"]
    role = payload["role"]

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[user {user_id}, {role}] echo: {data}")
    except WebSocketDisconnect:
        pass