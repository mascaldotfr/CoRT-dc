#!/usr/bin/env python3

# XMAS 2025. Quick'n dirty code, assumes UTC is the default timezone
# Crontab line: * * * * * cd ${HOME}/CoRT-dc && python3 2025_Xmas.py

from datetime import datetime as dt
import sys

notify_delay = 10 # minutes

now = dt.now()
now_ts = now.timestamp()

# event stops at this time
event_deadline = dt.fromisoformat("2026-01-02T12:00:00")
message_dc = ""
if now >= event_deadline and now.minute == 0 and now.hour % 3 == 0:
    message_dc = "Event is over, please disable me <@991767153571274833>!"
elif now.minute == 51 - notify_delay:
    # Orc appears at 51 every hour
    message_dc = f"Orcs' call for help in {notify_delay} minutes!"
elif now.minute == 41 - notify_delay and now.hour % 2 != 0:
    # Snow ball starts at 41 every odd UTC hour
    message_dc = f"Snowball war in {notify_delay} minutes!"
elif now.minute == 26 - notify_delay and now.hour % 2 == 0:
    # Sled Race starts at 26 every even UTC hour
    message_dc = f"Sled race in {notify_delay} minutes!"

if message_dc == "":
    sys.exit(1)

from libs import mydiscord
mydiscord.send_and_publish("events", message_dc)
