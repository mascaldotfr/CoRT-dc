# IRC setup

IRC is simpler that discord. While you may be used to eggdrops, we'll use
[irccat](https://github.com/irccloud/irccat) because it work with webhooks and
as such reuse mostly the same python codebase as discord. It's also very CPU
and RAM inexpensive.

### Pre-requisites

- Python 3 (with [CoRT's warstatus
  activated](https://github.com/mascaldotfr/CoRT/tree/main/warstatus)
  and [statistics](https://github.com/mascaldotfr/CoRT/tree/main/warstatus/stats)
  otherwise you'll need to deactivate them [here](irc_commands.py) in the code
  and ignore anything related to it later in the READMEs. Another option is to
  modify the code to fetch the json file from the API endpoints.
- irccat (i'll detail)
- tmux or screen

### IRCCAT

1. Download irccat at https://github.com/irccloud/irccat/releases/. If you need QuakeNet's Q cloaking
   [see my fork](https://github.com/mascaldotfr/irccat).
2. Extract it somewhere on your server (to a directory we'll later call `$IRCCAT`)
3. `cd $IRCCAT && chmod +x irccat`
4. In `$IRCCAT` you'll need a `irccat.json`, here is an example:

```json
{
  "http": {
    "listen": "localhost:8045",
    "tls": false,
    "tls_key": "",
    "tls_cert": "",
    "listeners": {
      "generic": {
        "secret": "",
        "strict": false
      }
    }
  },
  "irc": {
    "server": "irc.oftc.net:6697",
    "tls": true,
    "tls_skip_verify": false,
    "tls_client_cert": "",
    "tls_client_key": "",
    "nick": "CoRT-Bot",
    "realname": "CoRT-Bot",
    "server_pass": "",
    "identify_pass": "",
    "sasl_external": false,
    "sasl_login": "",
    "sasl_pass": "",
    "channels": ["#channel"],
    "keys": {}
  },
  "commands": {
    "auth_channel": "",
    "handler": "/where/is/CoRT-dc/irc_commands.py",
    "max_response_lines": 15
  }
}
```

5. In CORT-dc root directory, copy `secrets.py.example` to `secrets.py`, add
   the webhook url to the `irccat` variable, with the above config that's
   `http://localhost:8045/send`.
6. Open `screen` or `tmux` and run `cd $IRCCAT && ./irccat`. Your bot should be
   in the desired channel ; you can test it by typing `!rules`.
   Note that some may want to use a systemd service, which is not detailed here.

### AVAILABLE COMMANDS

[See the command dispatcher](irc_commands.py)

