# CoRT-dc

This includes all Discord stuff for Champions of Regnum, as of now:

- a bot that displays BZ status changes and next BZs, with countdowns (live @ https://discord.gg/DXDWKnZ2mw)
- a bot that displays bosses respawn time, with countdowns (live @ https://discord.gg/SBzmeycYdT)

It's released under the MIT License. Due to various issues with auto publishing
announcements through a third party bot, the interaction changed and is now
using discord.py itself instead of webhooks. See also the `legacy` branch.


I hope to document the setup later, as there is some changes.

---

**OLD DOCUMENTATION, SEE LEGACY BRANCH**



# CoRT-dc

This includes all Discord stuff for Champions of Regnum, as of now:

- a bot that displays BZ status changes and next BZs, with countdowns (live @ https://discord.gg/DXDWKnZ2mw)
- a bot that displays bosses respawn time, with countdowns (live @ https://discord.gg/SBzmeycYdT)

It's released under the MIT License

## Deployment

While i currently host that stuff, i would recommend, if you're capable to do
so, to self host these bots. They use very little resources and are not
permanent (launched through `cron`), making them able to work on tiny VPSes
with 128MB of RAM and 2GB disk space.

Deployment is pretty easy if you're used to Linux, Discord side can be painful.

### Pre-requisites

- Linux VPS or server (should work on windows but...), called VPS later
- Python 3, we only need base python, no external modules are used, thanks to
  discord webhooks (https://discord.com/developers/docs/resources/webhook)
- Cron activated (or do systemd timers if you prefer)

### Discord paperwork

*If you want to share your CoRT-dc channels with other servers, you'll need to
enable your community server, see
https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server*

Once enabled, create two channels, either text (local only) or announcement
(shared/community). Set the permissions so nobody can write in these two
channels but CoRT-dc. Let's call them `bz-status` and `bosses-status`.

Now create a webhook for each channel, a detailed guide can be found at
https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

Keep the webhook URLs somewhere, well need them later. **Note that these URLs
should be kept secret at any cost!**

As of now, Discord does **NOT** autopublish messages from webhooks in
announcement channels. You'll need to invite the bot "Auto Publisher" and configure
its permissions for your two channels accordingly, see the instructions at
https://discord.com/api/oauth2/authorize?client\_id=739823232651100180&permissions=76800&scope=bot

Once done you've just to install CoRT-dc in your server.

### VPS setup

You could use git, but i'm detailing the good old download method.

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
nextboss = 0
```

- Copy `secrets.py.example` to `secrets.py`, and add the webhook URLs you saved
  earlier for BZ and bosses. Chmod/Chown it accordingly.
- Now we'll trigger our first discord messages, issue the following commands:

```
cd /where/is/CoRT-dc
python3 bz.py # will only send a message if bz is on
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
