#!/usr/bin/env python3

import requests
import secrets

def send_message(channel, message):
    response = requests.post(secrets.webhooks[channel], json={"content":message})
    if response.status_code > 299:
        print(f'Failed to send message: {response.content}')
