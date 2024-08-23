#!/usr/bin/python3
import time
from subprocess import Popen
from wayfire import WayfireSocket as OriginalWayfireSocket
from wayfire.core.template import get_msg_template
from wayfire.extra.stipc import Stipc

class WayfireSocket(OriginalWayfireSocket):

    def hide_view(self, view_id):
        message = get_msg_template("hide-view/hide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

    def unhide_view(self, view_id):
        message = get_msg_template("hide-view/unhide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

TERMINAL_CMD = "wezterm"
TERMINAL_APPID = "org.wezfurlong.wezterm"
TERMINAL_WIDTH = 800
TERMINAL_HEIGHT = 600
VIEW_STICKY = True  # Show the terminal in all workspaces, set False to disable
VIEW_ALWAYS_ON_TOP = True  # Always on top even if another view gets the focus, set False to disable

sock = WayfireSocket()
stipc = Stipc(sock)

def configure_view(view, output):
    if TERMINAL_WIDTH and TERMINAL_HEIGHT:
        wa = output['workarea']
        geom = view['geometry']
        x = wa['x'] + wa['width'] // 2 - geom['width'] // 2
        y = wa['y'] + wa['height'] // 2 - geom['height'] // 2
        sock.configure_view(view["id"], x, y, TERMINAL_WIDTH, TERMINAL_HEIGHT)

def show_view(view):
    '''
    Required plugin: https://github.com/killown/wayfire-plugins/tree/main/plugins/hide-view    
    '''
    view_id = view["id"]
    sock.unhide_view(view_id)
    #configure_view(view, sock.get_focused_output())
    sock.set_view_always_on_top(view_id, VIEW_ALWAYS_ON_TOP)

def hide_view(view):
    '''
    Required plugin: https://github.com/killown/wayfire-plugins/tree/main/plugins/hide-view    
    '''
    view_id = view['id']
    sock.set_view_always_on_top(view_id, False)
    sock.hide_view(view_id)

# Find the terminal view by app ID
app_views = [v for v in sock.list_views() if v["app-id"] == TERMINAL_APPID]

if not app_views:
    # No terminal view found, so start a new one
    Popen(TERMINAL_CMD)
    time.sleep(1)
    new_views = [v for v in sock.list_views() if v["id"] == TERMINAL_APPID]

    if new_views:
        new_view = new_views[0]
        show_view(new_view)
    else:
        print("Failed to start new terminal!")

else:
    # Terminal view found, toggle its visibility
    view = app_views[0]
    if view["role"] != "toplevel":
        show_view(view)
    else:
        hide_view(view)

