from wayfire import WayfireSocket
import threading

def handle_output_events(socket):
    socket.watch(["output-gain-focus"])
    while True:
        msg = socket.read_message()
        print("Output Event:", msg)

def handle_plugin_events(socket):
    socket.watch(["plugin-activation-state-changed"])
    while True:
        msg = socket.read_message()
        print("Plugin Event:", msg)


def main():
    socket_1 = WayfireSocket()
    socket_2 = WayfireSocket()

    output_thread = threading.Thread(target=handle_output_events, args=(socket_1,))
    plugin_thread = threading.Thread(target=handle_plugin_events, args=(socket_2,))

    output_thread.start()
    plugin_thread.start()

    output_thread.join()
    plugin_thread.join()

if __name__ == "__main__":
    main()
1
