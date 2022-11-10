#!/usr/bin/env python3

# Copyright © 2022, mascal
# Released under the MIT license

from configparser import ConfigParser
from datetime import datetime as dt
import discord

"""
;test values to put in storage.ini file
Evendim = 1666803900
Thorkul = 1666745040
Daen = 1666890420
nextboss = 0
"""

respawn_time = 109 * 3600 # 109 hours
last_respawns = {}
next_respawns = {}
bosses = ["Evendim", "Thorkul", "Daen"]
now = dt.now()

storage = ConfigParser()
storage.read("storage.ini")

if int(storage.get("bosses", "nextboss")) >= now.timestamp():
    # a previous runtime already set up the current respawn times
    # and will only change when the next boss will respawn
    exit(1)

for boss in bosses:
    tried_respawn_ts = int(storage.get("bosses", boss))
    while True:
            tried_respawn_ts = tried_respawn_ts + respawn_time;
            tried_respawn_dt = dt.fromtimestamp(tried_respawn_ts)
            if tried_respawn_dt >= now:
                next_respawns[boss] = tried_respawn_ts
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
message = ""
for boss in next_respawns:
    message = f'{message}\n**{boss}:** <t:{next_respawns[boss]}> (~ <t:{next_respawns[boss]}:R>)'
discord.send_message("bosses", message);
