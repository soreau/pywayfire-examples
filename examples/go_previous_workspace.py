from wayfire import WayfireSocket
from wayfire.extra.ipc_utils import WayfireUtils
sock = WayfireSocket()
utils = WayfireUtils(sock)

def go_previous_workspace():
        grid_info = utils.get_active_workspace_info()
        current_x, current_y = grid_info['x'], grid_info['y']
        grid_width, grid_height = grid_info['grid_width'], grid_info['grid_height']
        previous = None
        if current_x > 0:
            previous =  {'x': current_x - 1, 'y': current_y  if current_x > 0 else grid_width - 1}
        if current_x == 0:
            previous = {'x': grid_width - 1, 'y': current_y - 1 if current_y > 0 else grid_height - 1}
        if previous:
            sock.set_workspace(previous)

go_previous_workspace()
