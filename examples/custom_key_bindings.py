import time
from wayfire import WayfireSocket 
sock = WayfireSocket()

response = sock.register_binding('<alt>')
binding_id = response['binding-id']
last_release_time = 0
MAX_DELAY = 0.5

while True:
    msg = sock.read_next_event()
    print(msg)
    if "event" in msg and msg["event"] == "command-binding":
        assert msg['binding-id'] == binding_id

        now = time.time()
        if now - last_release_time <= MAX_DELAY:
            print("toggle")
            sock.toggle_expo()
            last_release_time = now - 2 * MAX_DELAY # Prevent triple press
        else:
            print("reset")
            last_release_time = now
