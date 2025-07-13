#!/usr/bin/env python3

def run(data):
    import secrets
    if secrets.token == "":
        return
    bossesinfo = {
            "Evendim": {"icon": "<:eve:1393905397231783997>", "display": "Evendim"},
            "Thorkul": {"icon": "<:tk:1393905365112066068>", "display": "Thorkul"},
            "Daen": {"icon": "<:daen:1393905413900210256>", "display": "Daen Rha"},
            "Server": {"icon": ":recycle:", "display": "Server Reboot (<:eve:1393905397231783997><:tk:1393905365112066068><:daen:1393905413900210256>)"}
    }

    if data["type"] == "spawnsoon":
        boss = data["retval"]["name"]
        respawn_time = data["retval"]["time"]
        message = f'{bossesinfo[boss]["icon"]} **{bossesinfo[boss]["display"]}** is spawning soon: <t:{respawn_time}:R>'
    elif data["type"] == "nextrespawns":
        next_respawns = data["retval"]
        message = "**Next bosses respawns:**\n"
        for boss in next_respawns:
            message = f'{message}\n{bossesinfo[boss]["icon"]} **{bossesinfo[boss]["display"]}:** <t:{next_respawns[boss]}> (~ <t:{next_respawns[boss]}:R>)'
    from libs import mydiscord
    mydiscord.send_and_publish("bosses", message)
