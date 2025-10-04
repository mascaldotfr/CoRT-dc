#!/usr/bin/env python3

# Copyright © 2022-2024, mascal
# Released under the MIT license

from configparser import ConfigParser
from datetime import datetime as dt
import sys
import time

# Makes the program exit asap if nothing to display.  Returns a dict with the
# __type__ of returned value and a return value __retval__ which varies
# according to the type of output needs to be sent.
def get_respawns():
    next_respawns = {}
    bosses = ["Evendim", "Thorkul", "Daen", "Server"]
    now = time.time()
    warning_delay = 10 # Notify 10 minutes before a respawn

    storage = ConfigParser()
    storage.read("storage.ini")

    next_saved_respawn = int(storage.get("bosses", "nextboss"))

    next_respawn_in_minutes = dt.fromtimestamp(next_saved_respawn) - dt.fromtimestamp(now)
    next_respawn_in_minutes = int(next_respawn_in_minutes.total_seconds() / 60)
    if next_respawn_in_minutes == warning_delay:
        try:
            boss = storage.get("bosses", "nextbossname")
        except:
            # Should never happen if README.md is followed
            print("Unable to determine next boss name, will be fine by next respawn")
            return {"type": "quit"}
        respawn = {"name": boss, "time": next_saved_respawn}
        return {"type": "spawnsoon", "retval": respawn}

    if next_saved_respawn >= now:
        # a previous runtime already set up the current respawn times
        # and will only change when the next boss will respawn
        return {"type": "quit"}

    for boss in bosses:
        # storage contains previous respawns timestamps
        tried_respawn_ts = int(storage.get("bosses", boss))
        if boss == "Server":
            respawn_time = 168 * 3600 # 1 week
        else:
            respawn_time = 109 * 3600 # 109 hours
        while True:
                tried_respawn_ts = tried_respawn_ts + respawn_time
                if tried_respawn_ts >= now:
                    next_respawns[boss] = tried_respawn_ts
                    # set the last respawn for a given boss
                    storage.set("bosses", boss, str(tried_respawn_ts - respawn_time))
                    break
    # sort by spawning time
    next_respawns = dict(sorted(next_respawns.items(), key=lambda item: item[1]))

    # get the timestamp and name of the next boss to appear
    next_boss_appears_at = list(next_respawns.values())[0]
    next_boss_name = list(next_respawns.keys())[0]
    # store its respawn timestamp and name
    storage.set("bosses", "nextboss", str(next_boss_appears_at))
    storage.set("bosses", "nextbossname", str(next_boss_name))
    # rewrite ini file
    with open("storage.ini", "w") as storagefile:
                storage.write(storagefile)

    return {"type": "nextrespawns", "retval": next_respawns}

def display(data):
    import cortsecrets
    if cortsecrets.token == "":
        return
    bossesinfo = {
            "Evendim": {"icon": "<:eve:1393905397231783997>", "display": "Evendim"},
            "Thorkul": {"icon": "<:tk:1393905365112066068>", "display": "Thorkul"},
            "Daen": {"icon": "<:daen:1393905413900210256>", "display": "Daen Rha"},
            "Server": {"icon": ":recycle:", "display": "Server Reboot (<:eve:1393905397231783997><:tk:1393905365112066068><:daen:1393905413900210256>)"}
    }

    if data["type"] == "spawnsoon":
        boss = data["retval"]["name"]
        respawn_time = data["retval"]["time"]
        message = f'{bossesinfo[boss]["icon"]} **{bossesinfo[boss]["display"]}** is spawning soon: <t:{respawn_time}:R>'
    elif data["type"] == "nextrespawns":
        next_respawns = data["retval"]
        message = "**Next bosses respawns:**\n"
        for boss in next_respawns:
            message = f'{message}\n{bossesinfo[boss]["icon"]} **{bossesinfo[boss]["display"]}:** <t:{next_respawns[boss]}> (~ <t:{next_respawns[boss]}:R>)'
    from libs import mydiscord
    mydiscord.send_and_publish("bosses", message)

data = get_respawns()
if data["type"] != "quit":
    display(data)

