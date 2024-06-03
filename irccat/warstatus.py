#!/usr/bin/env python3

"""
It requires CoRT warstatus to run on the same machine, and modifying the
warstatus_json variable to point to your warstatus.json.

"""

from configparser import ConfigParser
import json
import os
import re
import sys
import time

from libs import irccat

warstatus_json = os.path.expanduser("~/public_drop/CoRT/warstatus/warstatus.json")

def remove_fort_nr(string):
    return re.sub(r" \(\d+\)$", "", string)

def format_item(string):
    realm = "%BLUE"
    string = remove_fort_nr(string)
    if re.search(r"(Ignis|Sam|Sha|Men)", string):
        realm = "%RED"
    elif re.search(r"(Syrtis|Her|Efe|Alg)", string):
        realm = "%DGREEN"
    # Remove fortifications numbers
    string = re.sub(r" \(\d+\)$", "", string)
    return f"""%BOLD{realm}{string}%NORMAL"""

def manage_ini():
    inifile = "storage.ini"
    storage = ConfigParser()
    storage.read(inifile)
    lastrun = int(storage.get("status", "lastrun"))
    storage.set("status", "lastrun", str(int(time.time())))
    with open(inifile, "w") as storagefile:
        storage.write(storagefile)
    if lastrun == 0:
        sys.exit(0)
    return lastrun

def send_message(message):
        irccat.send_message(message)

def run():
    lastrun = manage_ini()
    with open(warstatus_json) as response:
        message = ""
        data = json.loads(response.read())
        for event in data["events_log"]:
            if event["date"] > lastrun:
                if event["type"] in ("gem", "fort"):
                    captured = "captured"
                    if event["type"] == "gem":
                        event["name"] = f"""%UNDERLINE{event["location"]}%UNDERLINE%UNDERLINE's gem #{event["name"]}%NORMAL"""
                    if event["owner"] == event["location"]:
                        captured = "recovered"
                    owner = format_item(event["owner"])
                    name = format_item(event["name"])
                    send_message(f"""{owner} has {captured} {name}""")
                elif event["type"] == "relic":
                    location = "back in its altar"
                    if event["location"] != "altar":
                        location = "in transit"
                    name = format_item(event["name"] + "'s relic")
                    send_message(f"""{name} is {location}""")
                elif event["type"] == "wish":
                    location = format_item(event["location"])
                    send_message(f"""%REVERSE{location}%REVERSE made a dragon wish%NORMAL""")

def run_command():
    with open(warstatus_json) as response:
        message = ""
        data = json.loads(response.read())

        realms = ["Alsius", "Ignis", "Syrtis"]
        rcolors = ["%DGRAY", "%BLUE", "%RED", "%DGREEN"]
        # Gems numbers are in a different order : gem_\d.png
        rcolors_gems = ["%DGRAY", "%RED", "%BLUE", "%DGREEN"]

        for rid in range(0, len(realms)):
            # HEADER
            output = "%BOLD%BOLD" + format_item(realms[rid].ljust(6, ".")) + "%NORMAL "
            # FORTS
            output += "%BOLDF: %NORMAL"
            for fort in data["forts"]:
                if fort["location"] == realms[rid]:
                    fort_color = rcolors[realms.index(fort["owner"]) + 1]
                    fort_name = re.sub(r"(Great|Fort|Castle| )", "", fort["name"])
                    fort_name = remove_fort_nr(fort_name)[0:3]
                    output += f"""%BOLD{fort_color}{fort_name}%NORMAL """

            # GEMS
            output += "%BOLDG: %NORMAL"
            for gem in data["gems"][rid * 6:rid * 6 + 6]:
                gem_realm = re.search(r"gem_(\d).+", gem).groups()[0]
                color_gem = "%BOLD" + rcolors_gems[int(gem_realm)]
                output += f"""{color_gem}@%NORMAL"""
            output += " "
            # RELICS
            output += "%BOLDR: %NORMAL"
            for relic in data["relics"][realms[rid]]:
                if data["relics"][realms[rid]][relic] != None:
                    output += format_item(relic[0:3])
                else:
                    output += "%DGRAY" + relic[0:3] + "%NORMAL"
                output += " "
            send_message(output)
