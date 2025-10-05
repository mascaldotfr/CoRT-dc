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
- Decent understanding of said Linux system
- Python 3 (with the `requests` module; Debian: `python3-requests`)

### VPS setup

You could use git, but I am detailing the good old download method.

- Download the latest zip archive at https://github.com/mascaldotfr/CoRT-dc/archive/refs/heads/main.zip
- Extract it where you want

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
### Force display

If for some reasons you need to force the display of statuses, remove the
according file in `var`:

- `bz.json` for BZ
- `bosses.json` for bosses

Then call the according python script.

### Bosses respawn update

They're automatically up to date through
[CoRT](https://github.com/mascaldotfr/CoRT)'s API.

> [!NOTE]
> The updated respawn time will be displayed after the **next** boss respawn,
> which is ok because there is always a respawn between each boss respawn.
> You can still force display if you want.

### Events

Events are often one shot, quickly written stuff. You'll need to move them in
the main folder for them to work.
