#!/usr/bin/python3
import time
from subprocess import Popen
from wayfire import WayfireSocket as OriginalWayfireSocket
from wayfire.core.template import get_msg_template

class WayfireSocket(OriginalWayfireSocket):

    def hide_view(self, view_id):
        message = get_msg_template("hide-view/hide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

    def unhide_view(self, view_id):
        message = get_msg_template("hide-view/unhide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

TERMINAL_APPID = "kitty"
TERMINAL_CMD = "kitty"
TERMINAL_WIDTH = 800
TERMINAL_HEIGHT = 600
VIEW_STICKY = True # show the terminal in all workspaces, set False to disable
VIEW_ALWAYS_ON_TOP = True # always on top even if another view get the focus, Set False to disable

sock = WayfireSocket()

def find_view():
    hidden_view = shown_view = None
    for v in sock.list_views():
        if v['app-id'] == TERMINAL_APPID:
            print(v["role"])
            if v["role"] != "toplevel":
                hidden_view = v
            else:
                shown_view = v
    return hidden_view, shown_view

def configure_view(view, output):
    if TERMINAL_WIDTH == 0 or TERMINAL_HEIGHT == 0:
        return
    wa = output['workarea']
    geom = view['geometry']
    x = wa['x'] + wa['width'] // 2 - geom['width'] // 2
    y = wa['y'] + wa['height'] // 2 - geom['height'] // 2
    sock.configure_view(view["id"], x, y, TERMINAL_WIDTH, TERMINAL_HEIGHT)


def show_view(hidden_view):
    '''
    required plugin: https://github.com/killown/wayfire-plugins/tree/main/plugins/hide-view    
    '''
    id = hidden_view["id"]
    sock.unhide_view(id)
    configure_view(hidden_view, sock.get_focused_output())
    sock.set_view_always_on_top(id, True)

def hide_view(shown_view):
    '''
    required plugin: https://github.com/killown/wayfire-plugins/tree/main/plugins/hide-view    
    '''
    id = shown_view['id']
    sock.set_view_always_on_top(id, False)
    sock.hide_view(id)
    print("trying unhide")
   

hidden_view, shown_view = find_view()
if not shown_view and not hidden_view:
    Popen(TERMINAL_CMD, start_new_session=True)
    time.sleep(2)
    hidden_view, shown_view = find_view()
    if shown_view:
        show_view(shown_view)
    else:
        print("Failed to start new terminal!")
elif shown_view:
    hide_view(shown_view)
else:
    show_view(hidden_view)
