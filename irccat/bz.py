#!/usr/bin/env python3

def run(data):
    bz_on = data["bzon"]
    bz_ends_at = data["bzendsat"]
    import secrets
    if secrets.irccat != "":
        from libs import irccat
        from irccat import countdown as ct
        bz_status = "%DGREENBZ is ON" if bz_on else "%REDBZ is OFF"
        bz_status += "%NORMAL "
        if bz_on:
            timeleft = ct.countdown(bz_ends_at)
            bz_status += f"""and ends {timeleft}"""
        else:
            timeleft = ct.countdown(data["bzbegin"][0])
            bz_status += f"""and the next one begins {timeleft}"""

        irccat.send_message("%BOLD" + bz_status + "%NORMAL")

