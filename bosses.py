#!/usr/bin/env python3

# Copyright © 2022-2023, mascal
# Released under the MIT license

from configparser import ConfigParser
import sys
import time
import mydiscord

next_respawns = {}
bosses = {
        "Evendim": {"icon": ":ghost:", "display": "Evendim"},
        "Thorkul": {"icon": ":worm:", "display": "Thorkul"},
        "Daen": {"icon": ":alien:", "display": "Daen Rha"},
        "Server": {"icon": ":robot:", "display": "Server Reboot (:worm::alien::ghost:)"}
}
now = time.time()

storage = ConfigParser()
storage.read("storage.ini")

if int(storage.get("bosses", "nextboss")) >= now:
    # a previous runtime already set up the current respawn times
    # and will only change when the next boss will respawn
    sys.exit(1)

for boss in bosses.keys():
    # storage contains previous respawns timestamps
    tried_respawn_ts = int(storage.get("bosses", boss))
    if boss == "Server":
        respawn_time = 168 * 3600 # 1 week
        reboot_server_time = 1800 # 30 minutes reboot
    else:
        respawn_time = 109 * 3600 # 109 hours
        reboot_server_time = 0
    while True:
            tried_respawn_ts = tried_respawn_ts + respawn_time;
            if tried_respawn_ts >= now:
                next_respawns[boss] = tried_respawn_ts + reboot_server_time
                # set the last respawn for a given boss
                storage.set("bosses", boss, str(tried_respawn_ts - respawn_time))
                break
# sort by spawning time
next_respawns = dict(sorted(next_respawns.items(), key=lambda item: item[1]))

# get the timestamp of the next boss to appear
next_boss_appears_at = list(next_respawns.values())[0]
# store its respawn timestamp
storage.set("bosses", "nextboss", str(next_boss_appears_at))
# rewrite ini file
with open('storage.ini', 'w') as storagefile:
        storage.write(storagefile)
# create discord message
message = "**Next bosses respawns:**\n"
for boss in next_respawns:
    message = f'{message}\n{bosses[boss]["icon"]} **{bosses[boss]["display"]}:** <t:{next_respawns[boss]}> (~ <t:{next_respawns[boss]}:R>)'
mydiscord.send_and_publish("bosses", message)
