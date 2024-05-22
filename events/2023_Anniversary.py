#!/usr/bin/env python3

# Anniversary 2023 calls to war. Quick'n dirty code, meant to be executed 10
# minutes before the event. Times are CEST (UTC+2).

import sys
from datetime import datetime as dt
import mydiscord

now = dt.now()
currhour = int(now.strftime("%H"))
currday = int(now.strftime("%d"))

# event stops on the 01/06
if int(now.strftime("%m")) != 5:
    message = "Event is over, please disable me @mascal!"
    mydiscord.send_and_publish("test", message)
    sys.exit()
# event days
days = range(currday, 32)
# event hours
hours = [2, 16, 19, 23]

# number of timestamp issued
tstamps = 0
message = """
** Call to War starting in 10 minutes! **

Next Calls to War:
"""
try:
    for day in days:
        for hour in hours:
            # don't print passed calls of the current day
            if hour < currhour and day == currday:
                continue
            hdate = f'{day}/05/2023 {hour}:00'
            timestamp = int(dt.strptime(hdate, "%d/%m/%Y %H:%M").timestamp())
            message = f'{message}\n<t:{timestamp}:F>'
            tstamps += 1
            # only print the next 5 ones (roughly 24 hours)
            if tstamps == 5:
                raise
    # in case there are less than 5 calls left
    raise
except:
    mydiscord.send_and_publish("test", message)