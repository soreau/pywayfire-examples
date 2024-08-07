from wayfire import WayfireSocket
sock = WayfireSocket()
s = WayfireSocket()
plugins = sock.get_option_value("core/plugins")["value"]
plugin_name_to_disable = "pixdecor"

def disable_plugin(plugin_name):
    p = " ".join([i for i in plugins.split() if plugin_name not in i])
    s.set_option_values({"core/plugins":p})

def enable_plugin():
    s.set_option_values({"core/plugins":plugins})


sock.watch()
while True:
    msg = sock.read_message()
    if "event" in msg and "view" in msg:
        view = msg["view"]
        if view:
            view = sock.get_focused_view()
            if view["fullscreen"] is True:
                disable_plugin(plugin_name_to_disable)
            if view["fullscreen"] is False:
                enable_plugin()

