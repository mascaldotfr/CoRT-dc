#!/usr/bin/env python3

# Copyright © 2022-2025 mascal
# Released under the MIT license

import json
import sys
import time

status_file = "var/bz.json"
channel = "bz"

def get_data():
    import requests
    response = requests.get("https://cort.thebus.top/api/bin/bz/bz.php", timeout=10)
    return response.json()

def display():
    import cortsecrets
    if cortsecrets.token == "":
        return

    now = time.time()
    data = None
    # Bail out or get data. The try block ensures 1st run is ok
    try:
        with open(status_file) as f:
            old_status = json.load(f)
            if  (old_status["bzendsat"] != 0 and now > old_status["bzendsat"]) or\
                    now > old_status["bzbegin"][0]:
                data = get_data()
            else:
                sys.exit()
    except Exception as e:
        print("(Normal if it's your first run)", e)
        data = get_data()

    next_bzs_begin = data["bzbegin"]
    next_bzs_end = data["bzend"]
    bz_ends_at = data["bzendsat"]
    bz_on = data["bzon"]

    # display setup
    bz_status = ":white_check_mark: BZ is **ON**" if bz_on else ":x: BZ is **OFF**"
    bz_end_status = "Next one" if not bz_on else "Ending"
    bz_end_status_dt = bz_ends_at if bz_on else next_bzs_begin[0]
    bz_dctag_status = f'<t:{bz_end_status_dt}:R>'
    bz_dctag_status_full = f'<t:{bz_end_status_dt}:t>'

    message = f'{bz_status}. {bz_end_status} at {bz_dctag_status_full} (~ {bz_dctag_status}) \n\n'
    message = message + "**Next BZs:** \n"
    for next_bz in range(0, len(next_bzs_begin)):
        nextbz_begin_timestamp = f'<t:{next_bzs_begin[next_bz]}:F>'
        nextbz_end_timestamp = f'<t:{next_bzs_end[next_bz]}:t>'
        message = message + nextbz_begin_timestamp + "-" + nextbz_end_timestamp +"\n"

    from libs import mydiscord
    mydiscord.send_and_publish(channel, message)

    with open(status_file, "w") as f:
        json.dump(data, f)

display()
