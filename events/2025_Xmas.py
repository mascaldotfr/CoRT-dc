#!/usr/bin/env python3

# Anniversary 2024 ;  calls to war. Quick'n dirty code, meant to be executed 10
# minutes before the event. Times are CEST (UTC+2).
# Crontab line: * * * * * cd ${HOME}/CoRT-dc && python3 2025_Xmas.py

from datetime import datetime as dt
import sys

notify_delay = 10 # minutes

now = dt.now()
now_ts = now.timestamp()

snowball_epoch_ts = 1766317260
snowball_epoch_dt = dt.fromtimestamp(snowball_epoch_ts)
snowball_interval = 7200

race_epoch_ts = 1766327160
race_epoch_dt = dt.fromtimestamp(race_epoch_ts)
race_interval = 7200


# event stops at this time
event_deadline = dt.fromisoformat("2026-01-02T12:00:00")
message_dc = ""
if now >= event_deadline:
    message_dc = "Event is over, please disable me <@991767153571274833>!"
else:
    sbs_since_epoch = (now_ts - snowball_epoch_ts) // snowball_interval
    next_snowball_ts = int(snowball_epoch_ts + (sbs_since_epoch + 1) * snowball_interval)
    if round((next_snowball_ts - now_ts) / 60) == notify_delay:
        message_dc = f"Snowball war in {notify_delay} minutes ({next_snowball_ts})!"

    races_since_epoch = (now_ts - race_epoch_ts) // race_interval
    next_race_ts = int(race_epoch_ts + (races_since_epoch + 1) * race_interval)
    if round((next_race_ts - now_ts) / 60) == notify_delay:
        message_dc = f"Race in {notify_delay} minutes ({next_race_ts})!"

    if message_dc == "":
        sys.exit(1)

from libs import mydiscord
mydiscord.send_and_publish("test", message_dc)
