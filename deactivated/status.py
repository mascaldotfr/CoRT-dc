#!/usr/bin/env python3

"""
A clone of the official #status-ra

It requires CoRT warstatus to run on the same machine, and modifying the
warstatus_json variable to point to your warstatus.json.

Due to rate limits, you should not use an announcement channel if you run it.

Install:
    cp storage.ini.bootstrap storage.ini
    # Add the channel ID for "wz" in ../secrets.py
    # Install the following crontab line (see ../README.md)

Crontab line:
* * * * * cd /where/is/CoRT-dc/deactivated && python3 status.py
"""

from configparser import ConfigParser
import json
import os
import re
import sys
import time

# Import dynamically since it's not in the main folder
realroot = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, realroot)
import secrets
import mydiscord

warstatus_json = os.path.expanduser("~/public_drop/CoRT/warstatus/warstatus.json")

def format_item(string):
    realm = "blue"
    gemtxt = ""
    if re.search(r"(Ignis|Samal|Shaanarid|Menirah)", string):
        realm = "red"
    elif re.search(r"(Syrtis|Herbred|Eferias|Algaros)", string):
        realm = "green"
    if re.search(r"gem #\d$", string):
        gemtxt = ":gem:"
    elif re.search(r"relic$", string):
        gemtxt = ":moyai:"
    # Remove fortifications numbers
    string = re.sub(r" \(\d+\)$", "", string)
    return f"""{gemtxt}:{realm}_square: {string}"""

def manage_ini():
    inifile = "storage.ini"
    storage = ConfigParser()
    storage.read(inifile)
    lastrun = int(storage.get("status", "lastrun"))
    storage.set("status", "lastrun", str(int(time.time())))
    with open(inifile, "w") as storagefile:
        storage.write(storagefile)
    if lastrun == 0:
        mydiscord.send_and_publish("wz", "It's my first run, i'll display some events soon!")
        sys.exit(0)
    return lastrun

def main():
    lastrun = manage_ini()
    with open(warstatus_json) as response:
        message = ""
        data = json.loads(response.read())
        for event in data["events_log"]:
            if event["date"] > lastrun:
                if event["type"] in ("gem", "fort"):
                    captured = "captured"
                    if event["type"] == "gem":
                        event["name"] = f"""{event["location"]}'s gem #{event["name"]}"""
                    if event["owner"] == event["location"]:
                        captured = "recovered"
                    owner = format_item(event["owner"])
                    name = format_item(event["name"])
                    message += f"""**{owner}** has {captured} **{name}**\n"""
                elif event["type"] == "relic":
                    location = "back in its altar"
                    if event["location"] != "altar":
                        location = "in transit"
                    name = format_item(event["name"] + "'s relic")
                    message += f"""**{name}** is **{location}**\n"""
                elif event["type"] == "wish":
                    location = format_item(event["location"])
                    message += f""":dragon: **{location}** made a dragon wish :dragon:\n"""

        if message != "":
            mydiscord.send_and_publish("wz", message)

main()
