import datetime
import json
import time
import discord
from . import OsuAPIv2

data_p = json.loads(open('players.json', "r").read())
emotes = {
    "A": "<:A_:887380030450176030>",
    "B": "<:B_:887380030475362304>",
    "C": "<:C_:887380030718640179>",
    "D": "<:D_:887380030496309278>",
    "S": "<:S_:887380030303375381>",
    "X": "<:X_:887380030622162954>",
    "SH": "<:SH_:887380030185955359>",
    "XH": "<:XH_:887380030555037726>",

    "0": "<:hit0:929840139935580181>",
    "50": "<:hit50:929840032011935825>",
    "100": "<:hit100:929840054409506896>",
    "100k": "<:hit100k:929840070842789948>",
    "300": "<:hit300:929840088588906587>",
    "300g": "<:hit300g:929840115302424587>",

    "Arrow": "<:arrow:963200790279909466>",
    "On": "<:status_online:887380229985820732>",
    "Off": "<:status_offline:887380229713182741>",
    "WasSupporter": "<:hasSupporter:963811736325070928>",
    "Supporter": "<:supporter:963811550903283742>"
}

def generate_embed_score(score, kind: str = ""):
    # pprint(score, depth=2)
    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv2.get_data_beatmapset(beatmap.get('beatmapset_id'))
    
    # beurk change >>>
    if beatmapset is None:
        return print("beatmapset is None shrug")

    stats = score.get('statistics')
    user = score.get('user')

    username = user.get('username')
    title = beatmapset.get('title')

    print(f"{username} completed the map {title}")
    # wprint(f"{username} completed the map {title}")

    color = 0xff66aa
    for p in data_p:
        if data_p[p]['osu_id'] == user.get('id'):
            color = int(data_p[p]['color'], 16)

    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

    embed = discord.Embed(title="**" + title + "**",
                          url=beatmap.get('url'),
                          color=color,
                          timestamp=t
                          )

    # embed.set_thumbnail(url=beatmapset.get('covers').get('list'))
    # img_osu: "https://i.imgur.com/bnSSOS9.png"
    # img_mania: "https://i.imgur.com/NVkykfe.png"
    # img_taiko: "https://i.imgur.com/iSQFSTn.png"
    # img_ctb: "https://i.imgur.com/MjOv5Kd.png"

    if score.get("mode") == "mania":
        img_mode = "https://i.imgur.com/NVkykfe.png"
    elif score.get("mode") == "osu":
        img_mode = "https://i.imgur.com/bnSSOS9.png"
    elif score.get("mode") == "fruits":
        img_mode = "https://i.imgur.com/MjOv5Kd.png"
    else:
        img_mode = "https://i.imgur.com/iSQFSTn.png"

    embed.set_thumbnail(url=img_mode)
    embed.set_image(url=beatmapset.get('covers').get('card'))
    embed.set_author(name=f"{beatmap.get('status')} completed by {username}", url="https://osu.ppy.sh/users/"
                                                                                  + str(user.get('id')),
                     icon_url=user.get('avatar_url'))
    # ☆☆☆
    length = str(time.strftime('%M:%S', time.gmtime(int(beatmap.get("total_length")))))
    stars = beatmap.get('difficulty_rating')
    embed.add_field(name=" __Beatmap informations:__ ", value=f"\n **__Durée:__** `{length}` "
                                                              f"\n **__stars:__** `{stars}☆`", inline=False)

    if not score.get('mods'):
        mods = "No Mod"
    else:
        mods = ', '.join(score.get('mods'))

    if score.get("pp") is not None:
        pp = int(round(score.get('pp')))
    else:
        pp = 0

    emote_rank = emotes.get(score.get("rank"))
    embed.add_field(name=f"**__{kind}Score:__**", value=f"__rank:__{emote_rank}"
                                                        f"\n| `{int(stats.get('count_300')):03d}` {str(emotes.get('300'))} |- - - - - - - - - - - - - -| "
                                                        f"`{int(stats.get('count_geki')):03d}` {str(emotes.get('300g'))} |\n"
                                                        f"| `{int(stats.get('count_100')):03d}` {str(emotes.get('100'))} |- - - - - - - - - - - - - -| "
                                                        f"`{int(stats.get('count_katu')):03d}` {str(emotes.get('100k'))} |\n"
                                                        f"| `{int(stats.get('count_50')):03d}` {str(emotes.get('50'))} |- - - - - - - - - - - - - -| "
                                                        f"`{int(stats.get('count_miss')):03d}` {str(emotes.get('0'))} |"
                                                        f"\n| __pp:__ `{int(pp):03d}` pp |- - - - - - - - - - - -| "
                                                        f"__Mods:__ `{mods}`"
                                                        f"\n| __combo:__ `{int(score.get('max_combo')):04d}` x |- - - - - - - - -|"
                                                        f"__Accuracy:__ `{round(score.get('accuracy') * 100, 2)} %`",
                    inline=True)

    return embed


def get_binded(ctx):
    for p in data_p:
        if str(ctx.author.id) == str(data_p[p]["discord_id"]):
            return data_p[p]
    return None