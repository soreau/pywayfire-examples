from wayfire import WayfireSocket
from wayfire.extra.wpe import WPE 
import sys
sock = WayfireSocket() 
wpe = WPE(sock)

focused_view_id = sock.get_focused_view()["id"]

if "unpin" in sys.argv:
    id = sys.argv[-1]
    try:
        wpe.unpin_view(focused_view_id)
    except:
        print("view is not pinned")
    sys.exit(1)

wpe.pin_view(focused_view_id, "bottom", False)
sock.set_view_fullscreen(focused_view_id, True)

