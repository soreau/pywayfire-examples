import argparse
from wayfire import WayfireSocket

# Initialize WayfireSocket instances
sock = WayfireSocket()
s = WayfireSocket()
plugins = sock.get_option_value("core/plugins")["value"]

def disable_plugin(plugin_name):
    p = " ".join([i for i in plugins.split() if plugin_name not in i])
    s.set_option_values({"core/plugins": p})

def enable_plugin(plugin_name):
    p = plugins + " " +  plugin_name
    s.set_option_values({"core/plugins": p})

def main():
    parser = argparse.ArgumentParser(description="Manage Wayfire plugins.")
    parser.add_argument(
        "--disable",
        metavar="PLUGIN_NAME",
        type=str,
        help="Disable a specific plugin by name."
    )
    parser.add_argument(
        "--enable",
        metavar="PLUGIN_NAME",
        type=str,
        help="Enable a specific plugin by name."
    )
    
    args = parser.parse_args()

    if args.disable:
        disable_plugin(args.disable)
        print(f"Plugin '{args.disable}' has been disabled.")
    elif args.enable:
        enable_plugin(args.enable)
        print("The plugin {0} have been enabled.".format(args.enable))
    else:
        print("No action specified. Use --disable <plugin_name> or --enable.")

if __name__ == "__main__":
    main()

