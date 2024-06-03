#!/usr/bin/env python3

# Anniversary 2024 ;  calls to war. Quick'n dirty code, meant to be executed 10
# minutes before the event. Times are CEST (UTC+2).
# Crontab line: 50 15,18,22,1 * * * sleep 10 && cd ${HOME}/CoRT-dc && python3 2024_Anniversary.py

from datetime import datetime as dt
from datetime import timedelta as td
import sys
import textwrap

now = dt.now()

# event stops on the 03/06
event_deadline = dt.fromisoformat("2024-06-03T18:00:00")
if now >= event_deadline:
    message_dc = "Event is over, please disable me <@991767153571274833>!"
    message_irc = "Event is over, please disable me mascal!"
else:
    # event hours
    hours = [2, 16, 19, 23]

    # number of timestamp issued
    tstamps = 0
    message_irc = "Call to War starting in 10 minutes!"
    message_dc = textwrap.dedent(f"""
    ** {message_irc} **

    Next Calls to War:
    """)
    try:
        for day in (now, now + td(days=1)):
            for hour in hours:
                calldt = day.replace(hour=hour, minute=0, second=0)
                if calldt < now:
                    continue # Skip passed events of the day
                if calldt > event_deadline:
                    raise # Don't display next calls after the end of the event
                timestamp = int(calldt.timestamp())
                message_dc = f"""{message_dc}\n<t:{timestamp}:F>"""
                tstamps += 1
                if tstamps == 5:
                    raise # only print the next 5 ones (roughly 24 hours)
    except:
        pass

    if tstamps == 0 :
        # This should never happen if called at the right times
        print("No next calls to war to display", file=sys.stderr)
        sys.exit(1)


from libs import mydiscord
mydiscord.send_and_publish("events", message_dc)

import secrets
if secrets.irccat != "":
    from libs import irccat
    irccat.send_message("%REVERSE" + message_irc + "%NORMAL")
