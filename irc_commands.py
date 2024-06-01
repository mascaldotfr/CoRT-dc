#!/usr/bin/env python3

import os

nick = os.environ.get("IRCCAT_NICK")
#user = os.environ.get("IRCCAT_USER")
#host = os.environ.get("IRCCAT_HOST")
#channel = os.environ.get("IRCCAT_CHANNEL")
#respond_to = os.environ.get("IRCCAT_RESPOND_TO")
command = os.environ.get("IRCCAT_COMMAND")
args = os.environ.get("IRCCAT_ARGS")

os.chdir(os.path.dirname(__file__))

if command == "bz":
    from libs import bz
    from irccat import bz as ircbz
    data = bz.run()
    ircbz.run(data)
elif command in ("bosses", "boss"):
    from libs import bosses
    from irccat import bosses as ircboss
    ircboss.command_run()
elif command == "wz":
    from irccat import warstatus
    warstatus.run_command()
elif command in ("last", "stats", "stat"):
    from irccat import wstats
    wstats.run_command()
elif command in ("trout", "slap"):
    target = args.strip()
    if target == "CoRT-Bot":
        print(f"How dare you {nick} ?")
    elif len(args) > 0:
        print(f"\001ACTION slaps {args.strip()} around a bit with a large trout\001")
    else:
        print(f"!{command} <nickname>")
elif command in ("trainer", "site"):
    print("https://mascaldotfr.github.io/CoRT")
elif command == "code":
    print("https://github.com/mascaldotfr/CoRT-dc")
elif command == "mascal":
    print("A vos ordres Chef o>")
elif command == "rules":
    from libs import irccat
    target = "@" + nick + " "
    irccat.send_message(target + "%REVERSERULES%NORMAL")
    irccat.send_message(target + "1. Don't be an ass, use but not abuse the bot")
    irccat.send_message(target + "2. Avoid discussing hairy stuff (NSFW, politics, discrimination, doxxing)")
    irccat.send_message(target + "3. Posting fishy external links may lead to a ban")
    irccat.send_message(target + "4. mascal has the final say, but bans will be justified")
