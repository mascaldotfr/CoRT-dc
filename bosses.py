#!/usr/bin/env python3

# Copyright © 2022-2024, mascal
# Released under the MIT license

import sys

from libs import bosses

data = bosses.run()

if data["type"] == "quit":
    sys.exit() # Nothing to do

from discord import bosses
bosses.run(data)

from irccat import bosses
bosses.run(data)
