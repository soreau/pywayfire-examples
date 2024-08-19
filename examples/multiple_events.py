
from wayfire import WayfireSocket
import threading

def handle_general_events(socket):
    socket.watch(["event"])
    while True:
        msg = socket.read_message()
        print("General Event:", msg)

def handle_view_events(socket):
    socket.watch(["event", "view"])
    while True:
        msg = socket.read_message()
        print("View Event:", msg)

def handle_output_events(socket):
    socket.watch(["event", "output-gain-focus"])
    while True:
        msg = socket.read_message()
        print("Output Event:", msg)

def handle_plugin_events(socket):
    socket.watch(["event", "plugin-activation-state-changed"])
    while True:
        msg = socket.read_message()
        print("Plugin Event:", msg)


def main():
    socket_1 = WayfireSocket()
    socket_2 = WayfireSocket()
    socket_3 = WayfireSocket()
    socket_4 = WayfireSocket()

    general_thread = threading.Thread(target=handle_general_events, args=(socket_1,))
    view_thread = threading.Thread(target=handle_view_events, args=(socket_2,))
    output_thread = threading.Thread(target=handle_output_events, args=(socket_3,))
    plugin_thread = threading.Thread(target=handle_plugin_events, args=(socket_4,))

    general_thread.start()
    view_thread.start()
    output_thread.start()
    plugin_thread.start()

    general_thread.join()
    view_thread.join()
    output_thread.join()
    plugin_thread.join()

if __name__ == "__main__":
    main()
