from wayfire import WayfireSocket
from wayfire.extra.ipc_utils import WayfireUtils
import sys
sock = WayfireSocket()
utils = WayfireUtils(sock)

output_name = sys.argv[-1]
view_id = int(sys.argv[-2])

output_id = utils.get_output_id_by_name(output_name)
if output_id:
    wset = sock.get_output(output_id)["wset-index"]
    if view_id:
        sock.send_view_to_wset(view_id, wset)
