#!/usr/bin/env python3

# Copyright © 2022, mascal
# Released under the MIT license


from datetime import datetime as dt
from datetime import timezone as tz
from configparser import ConfigParser
import mydiscord


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

next_bzs_begin = [];
next_bzs_end = [];
bz_on = False;
bz_ends_at = 0;

now = dt.now(tz=tz.utc)
current_day = now.weekday()
current_hour = now.hour
tomorrow = current_day + 1 if current_day + 1 <= 6 else 0;
# get current bz status
for hour in range(0, len(bz_begin[current_day])):
    if ( current_hour >= bz_begin[current_day][hour] and
         current_hour < bz_end[current_day][hour]):
        bz_on = True
        bz_ends_at = dt.now(tz=tz.utc)
        bz_ends_at = bz_ends_at.replace(hour = bz_end[current_day][hour],
                                        minute = 0, second = 0)
        break
# compute future bzs
for day in [current_day, tomorrow]:
    for hour in range(0, len(bz_begin[day])):
        # skip passed BZ of th day
        if day == current_day and bz_begin[day][hour] <= current_hour:
            continue
        time_holder = dt.now(tz=tz.utc)
        day_offset = 0 if day == current_day else 1
        next_bzs_begin.append(time_holder.replace(day = time_holder.day + day_offset,
                                                  hour = bz_begin[day][hour], minute = 0,second = 0))
        time_holder = dt.now(tz=tz.utc)
        next_bzs_end.append(time_holder.replace(day = time_holder.day + day_offset,
                                                hour = bz_end[day][hour], minute = 0,second = 0))

# display setup
message = "";
bz_status = ":white_check_mark: BZ is **ON**" if bz_on else ":x: BZ is **OFF**"
bz_end_status = "Next one" if not bz_on else "Ending"
bz_end_status_dt = bz_ends_at if bz_on else next_bzs_begin[0]
bz_dctag_status = f'<t:{int(dt.timestamp(bz_end_status_dt))}:R>';
bz_dctag_status_full = f'<t:{int(dt.timestamp(bz_end_status_dt))}:t>';
message = message + f'{bz_status}. {bz_end_status} at {bz_dctag_status_full} (~ {bz_dctag_status}) \n\n'
message = message + "**Next BZs:** \n"
for next_bz in range(0, len(next_bzs_begin)):
    nextbz_begin_timestamp = f'<t:{int(dt.timestamp(next_bzs_begin[next_bz]))}:F>'
    nextbz_end_timestamp = f'<t:{int(dt.timestamp(next_bzs_end[next_bz]))}:t>'
    message = message + nextbz_begin_timestamp + "-" + nextbz_end_timestamp +"\n"

# only display in discord when status change
storage = ConfigParser()
storage.read("storage.ini")
# ConfigParser can't deal with booleans
str_bz_on = "1" if bz_on else "0"
if (storage.get("bz", "bz_on") != str_bz_on):
    storage.set("bz", "bz_on", str_bz_on)
    with open('storage.ini', 'w') as storagefile:
        storage.write(storagefile)
    mydiscord.send_and_publish("bz", message)
