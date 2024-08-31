import asyncio
import websockets
import json
from wayfire import WayfireSocket
from wayfire.extra.wpe import WPE
import socket
import struct
import ipaddress
import os

def get_local_network_range():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    netmask = '255.255.255.0'  # Assuming a common local netmask
    ip_bin = struct.unpack('>I', socket.inet_aton(local_ip))[0]
    netmask_bin = struct.unpack('>I', socket.inet_aton(netmask))[0]
    network_bin = ip_bin & netmask_bin
    network_address = socket.inet_ntoa(struct.pack('>I', network_bin))
    cidr_prefix = bin(netmask_bin).count('1')
    return f"{network_address}/{cidr_prefix}"

local_network_range = get_local_network_range()

ALLOWED_IP_RANGES = [
    local_network_range
]

def ip_in_allowed_range(ip):
    return any(ipaddress.ip_address(ip) in ipaddress.ip_network(range) for range in ALLOWED_IP_RANGES)

def call_method(method, args):
    num_args = len(args)
    if num_args == 0:
        result = method()
    elif num_args == 1:
        result = method(args[0])
    elif num_args == 2:
        result = method(args[0], args[1])
    elif num_args == 3:
        result = method(args[0], args[1], args[2])
    elif num_args == 4:
        result = method(args[0], args[1], args[2], args[3])
    elif num_args == 5:
        result = method(args[0], args[1], args[2], args[3], args[4])
    return result

async def handle_client(websocket, path):
    client_ip = websocket.remote_address[0]
    
    # Check if IP validation is enabled via environment variable
    ip_check_enabled = os.getenv('WAYFIRE_IPC_LAN_ONLY') is not None

    if ip_check_enabled and not ip_in_allowed_range(client_ip):
        await websocket.close()
        return

    sock = WayfireSocket()
    wpe = WPE(sock)

    async for message in websocket:
        command = message.split()[0]
        if command == "list_methods":
            result = dir(sock) + dir(wpe)
            json_result = json.dumps(result, default=str)
            await websocket.send(json_result)
            continue
        try:
            args = message.split(' ', 1)[1]
            args = args.split()
        except:
            args = []
            pass
        if hasattr(sock, command):
            method = getattr(sock, command)
            if callable(method):
                try:
                    result = call_method(method, args)
                    json_result = json.dumps(result, default=str)
                    await websocket.send(json_result)
                except Exception as e:
                    await websocket.send(json.dumps({"error": str(e)}))
            else:
                await websocket.send(json.dumps({"error": f"{command} is not a callable method"}))
        elif hasattr(wpe, command):
            method = getattr(wpe, command)
            if callable(method):
                try:
                    result = call_method(method, args)
                    json_result = json.dumps(result, default=str)
                    await websocket.send(json_result)
                except Exception as e:
                    await websocket.send(json.dumps({"error": str(e)}))
            else:
                await websocket.send(json.dumps({"error": f"{command} is not a callable method"}))
        else:
            await websocket.send(json.dumps({"error": f"Unknown command: {message}"}))

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8787)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
