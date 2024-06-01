#!/usr/bin/env python3

# Copyright © 2022-2024 mascal
# Released under the MIT license

from datetime import datetime as dt
import sys

from libs import bz

data = bz.run()
if data["mustdisplay"] == False:
    sys.exit()

from discord import bz
bz.run(data)

from irccat import bz
bz.run(data)
