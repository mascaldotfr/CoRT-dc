#!/usr/bin/env python3

import sys

import cortsecrets
import requests
def send_message(message):
    try:
        response = requests.post(cortsecrets.irccat, message)
        if response.status_code > 299:
            print(f'Failed to send message: {response.content}')
            sys.exit(1)
    except Exception as e:
        print("IRC failure" + repr(e))
        sys.exit(1)


