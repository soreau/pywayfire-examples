from wayfire.ipc import WayfireSocket 
from wayfire.extra.ipc_utils import WayfireUtils

sock = WayfireSocket()
utils = WayfireUtils(sock)

def get_previous_item(lst, current):
    if not lst:
        return None
    current_coords = (current['x'], current['y'])
    coords_list = [(item['x'], item['y']) for item in lst]
    if current_coords not in coords_list:
        return None
    current_index = coords_list.index(current_coords)
    previous_index = (current_index - 1) % len(coords_list)
    previous_coords = coords_list[previous_index]
    for item in lst:
        if (item['x'], item['y']) == previous_coords:
            return item

def remove_repeated_coordinates(lst):
    seen_coordinates = set()
    result = []
    for item in lst:
        coordinates = (item['x'], item['y'])
        if coordinates not in seen_coordinates:
            seen_coordinates.add(coordinates)
            result.append(item)
    return result

def get_workspaces_with_views():
    focused_output = sock.get_focused_output()
    monitor = focused_output["geometry"]
    ws_with_views = []
    views = utils.focused_output_views()

    if views:
        views = [
            view for view in views 
            if view["role"] == "toplevel" and not view["minimized"] and view["app-id"] != "nil" and view["pid"] > 0
        ]
        
        if views:
            grid_width = focused_output["workspace"]["grid_width"]
            grid_height = focused_output["workspace"]["grid_height"]
            current_ws_x = focused_output["workspace"]["x"]
            current_ws_y = focused_output["workspace"]["y"]

            for ws_x in range(grid_width):
                for ws_y in range(grid_height):
                    for view in views:
                        if utils.view_visible_on_workspace(
                            view["geometry"],
                            ws_x - current_ws_x,
                            ws_y - current_ws_y,
                            monitor
                        ):
                            ws_with_views.append({"x": ws_x, "y": ws_y, "view-id": view["id"]})
            return ws_with_views
    return []

workspaces = remove_repeated_coordinates(get_workspaces_with_views())
active_workspace = utils.get_active_workspace()
previous_workspace_with_views = get_previous_item(workspaces, active_workspace)
sock.set_workspace(previous_workspace_with_views)
