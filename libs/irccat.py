#!/usr/bin/env python3

import secrets
import requests
def send_message(message):
    try:
        response = requests.post(secrets.irccat, message)
        if response.status_code > 299:
            print(f'Failed to send message: {response.content}')
            sys.exit(1)
    except Exception as e:
        import sys
        print("IRC failure" + repr(e))
        sys.exit(1)


