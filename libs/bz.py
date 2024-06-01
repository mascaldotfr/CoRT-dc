# Copyright © 2022-2024 mascal
# Released under the MIT license

from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as timedelta
from configparser import ConfigParser

def run():
    # BZ beginning and ending time
    # MONDAY = 0 SUNDAY = 6, ALL TIMES ARE UTC
    bz_begin = [ 	[3, 13, 20],
                    [13, 18],
                    [13, 20],
                    [3, 13, 18],
                    [13, 20],
                    [3, 13, 20],
                    [13, 18] 	]

    bz_end = [  [6, 16, 23],
                [16, 21],
                [16, 23],
                [6, 16, 21],
                [17, 23],
                [6, 16, 23],
                [16, 21]	]

    next_bzs_begin = []
    next_bzs_end = []
    bz_on = False
    bz_ends_at = 0
    must_display = False

    now = dt.now(tz=tz.utc)
    current_day = now.weekday()
    current_hour = now.hour
    tomorrow = current_day + 1 if current_day + 1 <= 6 else 0
    # get current bz status
    for hour in range(0, len(bz_begin[current_day])):
        if (current_hour >= bz_begin[current_day][hour] and
            current_hour < bz_end[current_day][hour]):
            bz_on = True
            bz_ends_at = dt.now(tz=tz.utc)
            bz_ends_at = bz_ends_at.replace(hour=bz_end[current_day][hour],
                                            minute=0, second=0)
            break
    # compute future bzs
    for day in [current_day, tomorrow]:
        for hour in range(0, len(bz_begin[day])):
            # skip passed BZ of th day
            if day == current_day and bz_begin[day][hour] <= current_hour:
                continue
            day_offset = 0 if day == current_day else 1
            time_holder = dt.now(tz=tz.utc) + timedelta(days=day_offset)
            next_bzs_begin.append(time_holder.replace(hour=bz_begin[day][hour],
                                                      minute=0, second=0))
            next_bzs_end.append(time_holder.replace(hour=bz_end[day][hour],
                                                    minute=0, second=0))

    storage = ConfigParser()
    storage.read("storage.ini")
    # ConfigParser can't deal with booleans
    str_bz_on = "1" if bz_on else "0"
    # BZ status changed ? 
    if (storage.get("bz", "bz_on") != str_bz_on):
        storage.set("bz", "bz_on", str_bz_on)
        with open('storage.ini', 'w') as storagefile:
            storage.write(storagefile)
        # Tell caller that we must display the new BZ times
        must_display = True

    return {"bzbegin": next_bzs_begin,
            "bzend": next_bzs_end,
            "bzon": bz_on,
            "bzendsat": bz_ends_at,
            "mustdisplay": must_display}
