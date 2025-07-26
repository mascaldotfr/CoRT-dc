#!/usr/bin/env python3

def run(data):
    import cortsecrets
    if cortsecrets.token == "":
        return
    from datetime import datetime as dt

    next_bzs_begin = data["bzbegin"]
    next_bzs_end = data["bzend"]
    bz_ends_at = data["bzendsat"]
    bz_on = data["bzon"]

    # display setup
    bz_status = ":white_check_mark: BZ is **ON**" if bz_on else ":x: BZ is **OFF**"
    bz_end_status = "Next one" if not bz_on else "Ending"
    bz_end_status_dt = bz_ends_at if bz_on else next_bzs_begin[0]
    bz_dctag_status = f'<t:{int(dt.timestamp(bz_end_status_dt))}:R>'
    bz_dctag_status_full = f'<t:{int(dt.timestamp(bz_end_status_dt))}:t>'

    message = f'{bz_status}. {bz_end_status} at {bz_dctag_status_full} (~ {bz_dctag_status}) \n\n'
    message = message + "**Next BZs:** \n"
    for next_bz in range(0, len(next_bzs_begin)):
        nextbz_begin_timestamp = f'<t:{int(dt.timestamp(next_bzs_begin[next_bz]))}:F>'
        nextbz_end_timestamp = f'<t:{int(dt.timestamp(next_bzs_end[next_bz]))}:t>'
        message = message + nextbz_begin_timestamp + "-" + nextbz_end_timestamp +"\n"

    from libs import mydiscord
    mydiscord.send_and_publish("bz", message)

