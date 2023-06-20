# CoRT-dc

This includes all Discord stuff for Champions of Regnum, as of now:

- a bot that displays BZ status changes and next BZs, with countdowns (live @ https://discord.gg/DXDWKnZ2mw)
- a bot that displays bosses respawn time, with countdowns (live @ https://discord.gg/SBzmeycYdT)

It's released under the MIT License. A former version using webhooks can be
found in the `legacy` branch of the repo.

## Deployment

While I currently host that stuff, I would recommend, if you are capable to do
so, to self host these bots. They use very little resources and are not
permanent (launched through `cron`), making them able to work on tiny VPSes
with 128MB of RAM and 2GB disk space.

Deployment is pretty easy if you're used to Linux, Discord side can be painful.

### Pre-requisites

- Linux VPS or server (should work on windows but...), called VPS later
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

### VPS setup

You could use git, but I am detailing the good old download method.

- Download the latest zip archive at https://github.com/mascaldotfr/CoRT-dc/archive/refs/heads/main.zip
- Extract it where you want
- Modify storage.ini to initialise triggers:

```
[bz]
; set 1 if BZ is currently off, otherwise 0
bz_on = 1

[bosses]
Evendim = 1682107811
Thorkul = 1681656552
Daen = 1679839823
Server = 1686736800
nextboss = 0
```

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

Hopefully, you should see messages appear in the two channels. Now let's
automate it with cron. Edit your crontab (use a normal user for that):

```
crontab -e
```
And add the following lines:

```
0 * * * * cd /where/is/CoRT-dc/ && python3 bz.py
5,20,35,50 * * * * cd /where/is/CoRT-dc/ && python3 bosses.py
```

Basically this runs the bz script at the beginning of every hour, and the boss
one every 15 minutes (told you it was not resource demanding).
