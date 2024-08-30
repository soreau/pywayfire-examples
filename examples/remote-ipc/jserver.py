import asyncio
import websockets
import json
from wayfire import WayfireSocket

async def handle_client(websocket):
    sock = WayfireSocket()

    async for message in websocket:
        if hasattr(sock, message):
            method = getattr(sock, message)
            if callable(method):
                try:
                    result = method()  # Call the method
                    json_result = json.dumps(result, default=str)
                    await websocket.send(json_result)
                except Exception as e:
                    await websocket.send(json.dumps({"error": str(e)}))
            else:
                await websocket.send(json.dumps({"error": f"{message} is not a callable method"}))
        else:
            await websocket.send(json.dumps({"error": f"Unknown command: {message}"}))

async def main():
    server = await websockets.serve(handle_client, "localhost", 8787)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

