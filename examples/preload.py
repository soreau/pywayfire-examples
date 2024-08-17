#!/usr/bin/env python3
from wayfire import WayfireSocket as OriginalWayfireSocket
from wayfire.core.template import get_msg_template
from wayfire.extra.stipc import Stipc
import argparse
import time
from subprocess import Popen
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action')

add = subparsers.add_parser('add')
add.add_argument('APP', nargs='?', type=str)
add.add_argument('APPID', nargs='?', type=str)

remove = subparsers.add_parser('remove')
remove.add_argument('viewid', nargs='?', default=None)


class WayfireSocket(OriginalWayfireSocket):
    
    def hide_view(self, view_id):
        message = get_msg_template("hide-view/hide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

    def unhide_view(self, view_id):
        message = get_msg_template("hide-view/unhide")
        message["data"]["view-id"] = view_id
        return self.send_json(message)

sock = WayfireSocket()
stipc = Stipc(sock)

args = parser.parse_args()
APP = str(args.APP)
APPID = str(args.APPID)

if args.action == "add":
    Popen([APP])
    while True:
        id = [i["id"] for i in sock.list_views() if APPID == i["app-id"]]
        if id:
            id = id[-1]
            sock.hide_view(id)
            break
        time.sleep(1)

if args.action == "remove":
    id = [i["id"] for i in sock.list_views() if APPID == i["app-id"]][0]
    sock.unhide_view(args.viewid)


