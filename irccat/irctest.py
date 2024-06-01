#!/usr/bin/env python3

import os, sys
realroot = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, realroot)

import secrets

if secrets.irccat != "":
    from libs import irccat
    irccat.send_message("@mascal TEST")
