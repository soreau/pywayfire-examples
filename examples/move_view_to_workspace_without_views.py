from wayfire import WayfireSocket 
from wayfire.extra.ipc_utils import WayfireUtils 

sock = WayfireSocket()
utils = WayfireUtils(sock)

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

def go_next_workspace_with_views():
    workspaces = get_workspaces_with_views()
    if not workspaces:
        return

    active_workspace = sock.get_focused_output()["workspace"]
    active_workspace = {"x": active_workspace["x"], "y": active_workspace["y"]}

    next_ws = utils.get_next_workspace(workspaces, active_workspace)
    if next_ws:
        sock.set_workspace(next_ws)

def move_view_empity_workspace():
    # if workspace is empity, then go for a workspace with views
    vac = utils.get_views_from_active_workspace()
    views = [view for view in sock.list_views() if view["id"] in vac and view["role"] == "toplevel" and view["mapped"] is True]
    print(views)
    if not views:
        go_next_workspace_with_views()
        return 
    else:
        ws = utils.get_workspaces_without_views()[0]
        focused_view_id = sock.get_focused_view()["id"]
        sock.set_workspace({"x":ws[0], "y":ws[1]}, focused_view_id)

move_view_empity_workspace()
