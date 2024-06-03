#!/usr/bin/env python3

def run(data):
    import secrets
    if secrets.irccat != "":
        from libs import irccat
        if data["type"] == "spawnsoon":
            boss = data["retval"]["name"]
            message = f'%UNDERLINE{boss} is spawning in 10 minutes.%NORMAL'
            irccat.send_message(message)

def command_run():
    import secrets
    if secrets.irccat != "":
        from configparser import ConfigParser
        from datetime import datetime as dt
        from datetime import timedelta as timedelta
        from libs import irccat
        from irccat import countdown as ct

        bosses = ["Evendim", "Thorkul", "Daen", "Server"]
        next_respawns = {}
        message = ""

        storage = ConfigParser()
        storage.read("storage.ini")

        for boss in bosses:
            boss_prev_respawn = dt.fromtimestamp(int(storage.get("bosses", boss)))
            offset = timedelta(days=7) if boss == "Server" else timedelta(hours=109)
            boss_next_respawn = boss_prev_respawn + offset
            timeleft = ct.countdown(boss_next_respawn)
            message += f"%BOLD%PURPLE{boss}%NORMAL {timeleft} "

        irccat.send_message(message)


