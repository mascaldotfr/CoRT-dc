# CoRT-dc

This includes all Discord stuff for Champions of Regnum, as of now:
- a bot that displays BZ status changes and next BZs, with countdowns (live @ https://discord.gg/DXDWKnZ2mw)
- a bot that displays bosses respawn time, with countdowns (live @ https://discord.gg/SBzmeycYdT)

It's released under the MIT License. A former, simpler version using webhooks can be
found in the `legacy` branch of the repo.

## Deployment

While I currently host that stuff, I would recommend, if you are capable to do
so, to self host these bots. They use very little resources and are not
permanent (launched through `cron`), making them able to work on tiny VPSes
with 128MB of RAM and 2GB disk space.

Deployment is pretty easy if you're used to Linux, Discord side can be painful.

### Pre-requisites

- Linux VPS or server (should work on windows but...), called VPS later
- Decent understanding of said Linux system
- Python 3

### VPS setup

You could use git, but I am detailing the good old download method.

- Download the latest zip archive at https://github.com/mascaldotfr/CoRT-dc/archive/refs/heads/main.zip
- Extract it where you want
- Copy `storage.ini.bootstrap` to `storage.ini` and modify the `bz_on` variable
  according to the current BZ situation

### Discord deployment

The configuration for Discord is detailed [in that README](README.discord.md)

### Automate

Now let's automate it with cron. Edit your crontab (use a normal user for
that):

```
crontab -e
```
And add the following lines:

```
0 * * * * cd /where/is/CoRT-dc/ && python3 bz.py
* * * * * cd /where/is/CoRT-dc/ && python3 bosses.py
```

## Update respawns

- Open https://mascaldotfr.github.io/CoRT/bosses.html
- Press F12, the click on the console tab
- You'll get the previous respawn time that you can insert in `storage.ini` and
 `storage.ini.bootstrap`

### Events

Events are often one shot, quickly written stuff. You'll need to move them in
the main folder for them to work.
