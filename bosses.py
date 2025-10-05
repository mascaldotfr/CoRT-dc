#!/usr/bin/env python3

# Copyright © 2022-2025, mascal
# Released under the MIT license

import json
import sys
import time

status_file = "var/bosses.json"
channel = "bosses"

def get_data():
    import requests
    response = requests.get("https://cort.thebus.top/api/bin/bosses/bosses.php", timeout=10)
    return response.json()

def display():
    # Bail out if there is no discord token
    import cortsecrets
    if cortsecrets.token == "":
        return

    now = time.time()
    warning_delay = 10 # Notify 10 minutes before a respawn
    data = None # API data
    old_status = None # Cached API data
    next_respawn_in_minutes = 0 # Needed to notify at warning_delay

    # Bail out or get data and display stuff. The try block ensures 1st run is ok
    try:
        with open(status_file) as f:
            old_status = json.load(f)
            next_respawn_in_minutes = int((old_status["next_boss_ts"] - now) / 60)
            # Allow to bypass without data fetching if we need to just notify
            if next_respawn_in_minutes != warning_delay:
                if now > old_status["next_boss_ts"]:
                    data = get_data()
                else:
                    sys.exit()
            else:
                # There is a respawn soon, just use the cache
                data = old_status
    except Exception as e:
        print("(Normal if it's your first run)", e)
        data = get_data()

    # Time to show off
    from libs import mydiscord
    binfo = {
            "evendim": {"icon": "<:eve:1393905397231783997>", "display": "Evendim"},
            "thorkul": {"icon": "<:tk:1393905365112066068>", "display": "Thorkul"},
            "daen": {"icon": "<:daen:1393905413900210256>", "display": "Daen Rha"},
            "server": {"icon": ":recycle:", "display": "Server Reboot"}
    }

    if next_respawn_in_minutes == warning_delay:
        boss = data["next_boss"]
        respawn_time = data["next_boss_ts"]
        message = f'{binfo[boss]["icon"]} **{binfo[boss]["display"]}**'
        message += f' is spawning soon: <t:{respawn_time}:R>'
        mydiscord.send_and_publish(channel, message)
        # We leave, the cache update will occur at respawn (next block)
    else:
        # Display all next respawns
        # sort by spawning time
        next_respawns = sorted(data["next_spawns"].items(), key=lambda item: item[1][0])
        message = ["**Next bosses respawns:**\n"]
        for boss, spawns in next_respawns:
            message.append(f'{binfo[boss]["icon"]} **{binfo[boss]["display"]}:** <t:{spawns[0]}> (~ <t:{spawns[0]}:R>)')

        mydiscord.send_and_publish(channel, "\n".join(message))

        with open(status_file, "w") as f:
            json.dump(data, f)

display()
