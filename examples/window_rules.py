from wayfire import WayfireSocket
sock = WayfireSocket()
sock.watch()

view = None

def match_view(app_id):
    if view["app-id"] == app_id:
        return True

#build your window rules here, the setup is just here
def window_rules(view):
    if match_view("kitty"):
        #set always on top
        sock.set_view_always_on_top(view["id"], True)
        #full screen on start
        sock.set_view_fullscreen(view["id"])
    if match_view("Picture-in-Picture"):
        #set the view always on top 
        sock.set_view_always_on_top(view["id"], True)
        #move the view to workspace 2
        sock.set_workspace({"x":0, "y":1}, view["id"])
        #switch back to workspace 1
        sock.set_workspace({"x":0, "y":0})

#you dont need to touch this
while True:
    msg = sock.read_message()
    if "event" in msg and "view" in msg:
        print(msg)
        view = msg["view"]
        if view:
            window_rules(view)

