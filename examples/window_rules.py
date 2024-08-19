from wayfire import WayfireSocket

class AdvancedWindowRules:
    def __init__(self):
        self.rule = WayfireSocket()
        self.rule.watch(["event"])
        self.view = None
        self.id = None

    def match_view(self, app_id):
        return self.view and self.view["app-id"] == app_id

    def view_mapped(self, msg):
        # When a new view is created (mapped)
        self.view = msg["view"]
        self.id = self.view["id"]

        if self.match_view("kitty"):
            self.rule.set_view_fullscreen(self.id, True)

        if self.match_view("Picture-in-Picture"):
            self.rule.set_view_always_on_top(self.id, True)
            self.rule.set_workspace({"x": 0, "y": 1}, self.id)
            self.rule.set_workspace({"x": 0, "y": 0})

    def focused_view_rule(self, msg):
        focused_view = msg["view"]
        focused_view_id = focused_view["id"]

        if self.match_view("kitty"):
            self.rule.set_view_fullscreen(focused_view_id, True)

    def output_gain_focus(self, msg):
        # Add code here to handle when a new output (monitor) gains focus
        pass

    def plugin_activation_state_changed(self, msg):
        # Add code here to handle when a plugin is activated or deactivated
        pass

    def view_unmapped(self, msg):
        # Add code here to handle when a view is closed (unmapped)
        pass

    def view_workspace_changed(self, msg):
        # Add code here to handle when a view changes its workspace
        pass

    def view_geometry_changed(self, msg):
        # Add code here to handle when a view's geometry changes
        pass

    def handle_events(self, msg):
        event = msg["event"]

        if event == "focused_view":
            self.focused_view_rule(msg)
        elif event == "output-gain-focus":
            self.output_gain_focus(msg)
        elif event == "plugin-activation-state-changed":
            self.plugin_activation_state_changed(msg)
        elif event == "view-mapped":
            self.view_mapped(msg)
        elif event == "view_unmapped": 
            self.view_unmapped(msg)
        elif event == "wset-workspace-changed":
            self.view_workspace_changed(msg)
        elif event == "view-geometry-changed":
            self.view_geometry_changed(msg)

    def run(self):
        while True:
            msg = self.rule.read_message()
            if "event" in msg:
                self.handle_events(msg)

# Instantiate and run the window rules
window_rules = AdvancedWindowRules()
window_rules.run()

