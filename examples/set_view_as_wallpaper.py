from wayfire import WayfireSocket
from wayfire.extra.wpe import WPE 
sock = WayfireSocket() 
wpe = WPE(sock)

focused_view_id = sock.get_focused_view()["id"]
wpe.pin_view(focused_view_id, "bottom", False, 0, 0)
sock.set_view_sticky(focused_view_id, True)
sock.set_view_fullscreen(focused_view_id, True)
