import asyncio
import websockets
import json
from wayfire import WayfireSocket

ALLOWED_IP_RANGES = [
    "192.168.0.0/16",
    "10.0.0.0/8",
    "172.16.0.0/12"
]

def ip_in_allowed_range(ip):
    from ipaddress import ip_address, ip_network
    return any(ip_address(ip) in ip_network(range) for range in ALLOWED_IP_RANGES)

async def handle_client(websocket, path):
    client_ip = websocket.remote_address[0]

    if not ip_in_allowed_range(client_ip):
        await websocket.close()
        return

    sock = WayfireSocket()
    async for message in websocket:
        if hasattr(sock, message):
            method = getattr(sock, message)
            if callable(method):
                try:
                    result = method()
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

