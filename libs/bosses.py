# Copyright © 2022-2024, mascal
# Released under the MIT license

from configparser import ConfigParser
from datetime import datetime as dt
import sys
import time

# Makes the program exit asap if nothing to display.  Returns a dict with the
# __type__ of returned value and a return value __retval__ which varies
# according to the type of output needs to be sent.
def run():
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
