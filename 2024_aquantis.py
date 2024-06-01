#!/usr/bin/env python3

# Warn when the legendary aquantis pops up. Must be called at xx:57

from datetime import datetime as dt

now = dt.now()
message = "The hourly Aquantis respawn is in 10 minutes!"

if now >= dt.fromisoformat("2024-06-03T18:00:00"):
    message = "Event is over, please disable me <@991767153571274833> / mascal!"


from libs import mydiscord
mydiscord.send_and_publish("events2", "**" + message + "**")

import secrets
if secrets.irccat != "":
    from libs import irccat
    irccat.send_message("%REVERSE" + message + "%NORMAL")
