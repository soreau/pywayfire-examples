#!/usr/bin/python3
import os
import time
from subprocess import Popen
from wayfire.ipc import *

TERMINAL_APPID = "foot"
TERMINAL_CMD = "foot"
TERMINAL_WIDTH = 1000
TERMINAL_HEIGHT = 600
VIEW_STICKY = True # show the terminal in all workspaces, set False to disable
VIEW_ALWAYS_ON_TOP = True # always on top even if another view get the focus, Set False to disable

addr = os.getenv('WAYFIRE_SOCKET')
sock = WayfireSocket(addr)

def find_view():
    hidden_view = shown_view = None
    for v in sock.list_views():
        if v['app-id'] == TERMINAL_APPID:
            if v['minimized']:
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
    sock.set_view_sticky(view["id"], VIEW_STICKY)
    sock.set_view_always_on_top(view["id"], VIEW_ALWAYS_ON_TOP)

def show_view(hidden_view):
    sock.set_view_minimized(hidden_view['id'], False)
    configure_view(hidden_view, sock.get_focused_output())

def hide_view(shown_view):
    sock.set_view_minimized(shown_view['id'], True)

hidden_view, shown_view = find_view()
if not shown_view and not hidden_view:
    Popen(TERMINAL_CMD, start_new_session=True)
    time.sleep(1)
    hidden_view, shown_view = find_view()
    if shown_view:
        show_view(shown_view)
    else:
        print("Failed to start new terminal!")
elif shown_view:
    hide_view(shown_view)
else:
    show_view(hidden_view)
