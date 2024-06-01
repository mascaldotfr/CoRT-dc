#!/usr/bin/env python3

"""
It requires CoRT warstatus and stats to run on the same machine, and modifying
the warstatus_json variable to point to your warstatus.json.

"""

from datetime import datetime as dt
import json
import os
import re

from libs import irccat
from irccat import countdown as ct

stats_json = os.path.expanduser("~/public_drop/CoRT/warstatus/stats/statistics.json")

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

def run_command():
    with open(stats_json) as response:
        message = ""
        data = json.loads(response.read())

        realms = ["Alsius", "Ignis", "Syrtis"]
        rcolors = ["%DGRAY", "%BLUE", "%RED", "%DGREEN"]
        data = data[-1]
        lines = {"Inva": "", "Gem": "", "Wish": ""}
        for rid in range(0, len(realms)):
            realm = realms[rid]
            last1 = {}
            last1["Inva"] = data[realm]["invasions"]["last"]["date"]
            last1["Gem"] = data[realm]["gems"]["stolen"]["last"]
            last1["Wish"] = data[realm]["wishes"]["last"]
            for last in last1:
                date = dt.fromtimestamp(last1[last])
                time = ct.countdown(date, reverse=True).rjust(22)
                lines[last] += "%BOLD" + rcolors[rid+1] + time  + "%NORMAL "
        for line in lines:
                irccat.send_message("%BOLD%PURPLE" + line.ljust(4, ".") + "%NORMAL " + lines[line])
