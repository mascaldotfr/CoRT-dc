# Discord setup

### Pre-requisites

- Python 3 with the `discord` (discord.py) module
- Cron activated (or do systemd timers if you prefer)
- Developer mode should be activated (see https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
- Basic knowledge of discord server management

### Discord paperwork

*If you want to share your CoRT-dc channels with other servers, you'll need to
enable your community server, see
https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server*

Once you get your server, create two channels, either text (local only) or
announcement (shared/community). Let's call them `bz-status` and
`bosses-status`.

### Create an Application (bot) and make it join your server

You need to create a bot account from your own account.

See https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro

At stage 6, give the following permissions to the bot:

- "Send Messages"
- "Manage Messages"

At this point, your should have your bot in your server member list.

### Set the channels permissions

Doc: https://support.discord.com/hc/en-us/articles/10543994968087-Channel-Permissions-Settings-101

You may have noted that your bot has a specific role, for each channels allow
it to:

- "View Channel"
- "Send Messages"
- "Manage Messages"

Set the permissions of `@everyone` so nobody can write in these two channels but
CoRT-dc (and you as the server owner).

Time to install the bot on your VPS now.

## System setup


- Copy `secrets.py.example` to `secrets.py`, add the secret token you got when
  creating the bot (you can regenerate it if lost), the various channels IDs
  and the server ID; see the developer link in *Pre-requisites* that explains
  how to get them. Leave the `test` channel ID as-is, it is used for development.
  Chmod/Chown it accordingly.
- Now we will trigger our first discord messages, issue the following commands:

```
cd /where/is/CoRT-dc
python3 bz.py
python3 bosses.py
```
Hopefully, you should see messages appear in the two channels.
