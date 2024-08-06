from wayfire import WayfireSocket
rule = WayfireSocket()
rule.watch()

view = None
id = None
def match_view(app_id):
    if view["app-id"] == app_id:
        return True

#build your window rules here, the setup is just here
def window_rules(view):
    id = view["id"]
    if match_view("kitty"):
        rule.set_view_always_on_top(id, True)
        rule.set_view_fullscreen(id)
    if match_view("Picture-in-Picture"):
        rule.set_view_always_on_top(id, True)
        rule.set_workspace({"x":0, "y":1}, id)
        rule.set_workspace({"x":0, "y":0})

#you dont need to touch this
while True:
    msg = rule.read_message()
    if "event" in msg and "view" in msg:
        view = msg["view"]
        if view:
            window_rules(view)

