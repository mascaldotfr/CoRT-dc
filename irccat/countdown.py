#!/usr/bin/env python3

def countdown(date, reverse=False):
        from datetime import datetime as dt
        from datetime import timezone as tz
        td = None
        if reverse == False:
            td = date.astimezone(tz=tz.utc) - dt.now().astimezone(tz=tz.utc)
        else:
            td = dt.now().astimezone(tz=tz.utc) - date.astimezone(tz=tz.utc)
        retval = str(td).split(".")[0]
        return "in " + retval if reverse == False else retval + " ago"
