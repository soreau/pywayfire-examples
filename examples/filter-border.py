from wayfire import WayfireSocket
from wayfire.extra.wpe import WPE 

sock = WayfireSocket()
wpe = WPE(sock)
shader_path = "/path/to/border"

# will apply the border only for the focused view
id = sock.get_focused_view()["id"]

# apply the effect
wpe.filters_set_view_shader(id, shader_path)
