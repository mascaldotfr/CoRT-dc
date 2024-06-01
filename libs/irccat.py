#!/usr/bin/env python3

import secrets
import requests
def send_message(message):
    response = requests.post(secrets.irccat, message)
    if response.status_code > 299:
        print(f'Failed to send message: {response.content}')

