from wayfire import WayfireSocket 
from wayfire.extra.ipc_utils import WayfireUtils 

sock = WayfireSocket()
utils = WayfireUtils(sock)
ws = utils.get_workspaces_without_views()[0]
print(ws)
focused_view_id = sock.get_focused_view()["id"]
sock.set_workspace({"x":ws[0], "y":ws[1]}, focused_view_id)


