#!/usr/bin/env python3

# Copyright © 2022-2023, mascal
# Released under the MIT license

import discord
import secrets

client = discord.Client(intents=discord.Intents.default())

def send_and_publish(target="test", msg="message"):
    @client.event
    async def on_ready():
        channel = client.get_channel(secrets.channels[target])
        await channel.send(msg)
        # Don't publish when testing things or i would hit the rate limit
        if target != "test":
            async for message in channel.history(limit=1):
                last_message = message
            await message.publish()
        await client.close()
    try:
        client.run(secrets.token)
    except Exception as e:
        import sys
        print("Discord failure" + repr(e))
        sys.exit(1)

