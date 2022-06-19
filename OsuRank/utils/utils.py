import datetime
import json
import time
import discord
import requests
import rosu_pp_py
import enum
from pprint import pprint
from . import OsuAPIv3

data_p = json.loads(open('players.json', "r").read())
osu_modes = ["mania", "osu", "fruits", "taiko"]
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

def generate_embed_score(score, kind: str = "", color: int = 0xff66aa):
    # pprint(score, depth=2)
    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv3.API().get_beatmapset(beatmap.get('beatmapset_id'))
    
    # beurk change >>>
    if beatmapset is None:
        return print("beatmapset is None shrug")

    stats = score.get('statistics')
    user = score.get('user')

    username = user.get('username')
    title = beatmapset.get('title')

    print(f"{username} completed the map {title}")
    # wprint(f"{username} completed the map {title}")
            

    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

    embed = discord.Embed(title=f"**{title}**",
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
    embed.set_image(url=beatmapset['covers'].get('card'))
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

# ============================= #
#                               #
#          AIKA v1.1.5          #
#                               #
# ============================= #
def generate_embed_score_2(score, kind: str = "", color: int = 0xff66aa):

    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv3.API().get_beatmapset(beatmap.get('beatmapset_id'))
    
    pprint(score)
    pprint(beatmapset)

    stats = score.get('statistics')
    user = score.get('user')

    username = user.get('username')
    
    print(f"{username} completed the map {beatmapset.get('title')}")
    # wprint(f"{username} completed the map {title}")
            

    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

    embed = discord.Embed(title=f"**{beatmapset.get('artist')} - {beatmapset.get('title')} \n[{beatmap.get('version')}]**",url=beatmap.get('url'),
                          color=color,timestamp=t)
    
    if score.get("mode") == "mania":
        img_mode = "https://i.imgur.com/NVkykfe.png"
    elif score.get("mode") == "osu":
        img_mode = "https://i.imgur.com/bnSSOS9.png"
    elif score.get("mode") == "fruits":
        img_mode = "https://i.imgur.com/MjOv5Kd.png"
    else:
        img_mode = "https://i.imgur.com/iSQFSTn.png"

    embed.set_thumbnail(url=img_mode)
    embed.set_image(url=beatmapset['covers'].get('card'))
    
    embed.set_author(name=f"[☆] {username} {kind} osu!{score.get('mode')} play.", url=f"https://osu.ppy.sh/users/{user.get('id')}", icon_url=user.get('avatar_url'))
    
    # ☆☆☆
    length = str(time.strftime('%M:%S', time.gmtime(int(beatmap.get("total_length")))))
    stars = float(beatmap.get('difficulty_rating'))
    emote_rank = emotes.get(score.get("rank"))
    if score.get("pp") is not None:
        pp = float(round(score.get('pp'), 2))
    else:
        pp = 0
    
    if not score.get('mods'):
        mods = "NM"
    else:
        mods = ', '.join(score.get('mods'))
        
    best_combo = int(beatmap.get('count_circles')) + int(beatmap.get('count_sliders')) + int(beatmap.get('count_spinners'))

    embed.add_field(name="Score informations", value=f" ▸  {emote_rank} **{round(score.get('accuracy') * 100, 2)}% {pp}pp** +{mods} {int(score.get('max_combo'))}/{best_combo}x"
                                                     f"\n ▸ {{ {int(stats.get('count_100'))}x100, {int(stats.get('count_50'))}x50, {int(stats.get('count_miss'))}xM }} ", 
                    inline=False)

    emote_rank = emotes.get(score.get("rank"))
    embed.add_field(name=f"Beatmap informations", value=f"**{str(beatmapset.get('status')).capitalize()} ⭐ {stars} | {length} @ 🎵 {float(beatmap.get('bpm'))}**"
                                                        f"\n**AR** {float(beatmap.get('ar'))} **OD** {float(beatmap.get('accuracy'))} **[[Download](https://akatsuki.pw/d/{beatmapset.get('id')})]**",
                    inline=False)
    
    embed.set_footer(text="(Aika version)")
    
    return embed


# ============================= #
#                               #
#              owo!             #
# osu!std only                  #
# ============================= #
def generate_embed_score_3(score, kind: str = "", color: int = 0xff66aa):

    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv3.API().get_beatmapset(beatmap.get('beatmapset_id'))


    stats = score.get('statistics')

    mods = score.get('mods')
    if mods == None:
        mods = ["NM"]
    
    # ☆☆☆
    emote_rank = emotes.get(score.get("rank"))
    accuracy = score.get('accuracy') * 100
    
    open("temp.osu", "wb" ).write(requests.get(f"https://osu.ppy.sh/osu/{beatmap.get('id')}").content)
    calculator = rosu_pp_py.Calculator("temp.osu")
    
    ParamNormal = rosu_pp_py.ScoreParams(acc=accuracy, mods=sum([Mods[k].value for k in mods]), n300=stats.get('count_300'), n100=stats.get('count_100'), n50=stats.get('count_50'), nMisses=stats.get('count_miss'), nKatu=stats.get('count_katu'), combo=score.get("max_combo"), score=score.get('score'))
    ParamFC = rosu_pp_py.ScoreParams(acc=accuracy, mods=sum([Mods[k].value for k in mods]))
    
    result = calculator.calculate([ParamNormal, ParamFC])
    print(result[0])
    
    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

    embed = discord.Embed(color=color, timestamp=t, 
                          description=f" ► {emote_rank} ▸ **{round(result[0].pp, 2)}pp** ({round(result[1].pp, 2)}pp for {round(accuracy, 2)}% FC) ▸ {round(accuracy, 2)}%"
                                      f"\n ► {score.get('score'):,} ▸ x{int(score.get('max_combo'))}/{result[1].maxCombo} ▸ [{int(stats.get('count_300'))}/{int(stats.get('count_100'))}/{int(stats.get('count_50'))}/{int(stats.get('count_miss'))}]")
    
    embed.set_thumbnail(url=beatmapset['covers'].get('list'))
    embed.set_author(name=f"{beatmapset.get('title')} [{beatmap.get('version')}]  + {', '.join(mods)} [{float(beatmap.get('difficulty_rating'))}★]", url=beatmap.get('url'), icon_url=score['user'].get('avatar_url'))
    embed.set_footer(text="(owo! version)")
    
    return embed


# ============================= #
#                               #
#           Bathbot!            #
# osu!std only                  #
# ============================= #
def generate_embed_score_4(score, kind: str = "", color: int = 0xff66aa):

    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv3.API().get_beatmapset(beatmap.get('beatmapset_id'))


    stats = score.get('statistics')
    # pprint(score)
    
    # score_id = score.get('id')

    mods = score.get('mods')
    # ☆☆☆
    emote_rank = emotes.get(score.get("rank"))
    accuracy = score.get('accuracy') * 100
    user = score['user']
    user_stats = OsuAPIv3.API().get_user(user=user.get('id'))["statistics"]
    
    best_scores = OsuAPIv3.API().get_user_score(user=user.get('id'), score_type="best", offset="20", limit=150, mode=score.get('mode'))
    desc = ""
    a = 0
    for s in best_scores:
        a += 1
        if score.get('best_id') == s.get('id'):
            desc = f" ► Personnal best #{a}"
    
    open("temp.osu", "wb" ).write(requests.get(f"https://osu.ppy.sh/osu/{beatmap.get('id')}").content)
    calculator = rosu_pp_py.Calculator("temp.osu")
    
    ParamNormal = rosu_pp_py.ScoreParams(acc=accuracy, mods=sum([Mods[k].value for k in mods]), n300=stats.get('count_300'), n100=stats.get('count_100'), n50=stats.get('count_50'), nMisses=stats.get('count_miss'), nKatu=stats.get('count_katu'), combo=score.get("max_combo"), score=score.get('score'))
    ParamFC = rosu_pp_py.ScoreParams(mods=sum([Mods[k].value for k in mods]), n300=stats.get('count_300'), n100=stats.get('count_100'), n50=stats.get('count_50'), nMisses=0)
    ParamBEST = rosu_pp_py.ScoreParams(mods=sum([Mods[k].value for k in mods]))
    
    result = calculator.calculate([ParamNormal, ParamFC, ParamBEST])
    print(result[0])
    
    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

    embed = discord.Embed(title=f"**{beatmapset.get('artist')} - {beatmapset.get('title')} [{beatmap.get('version')}]**",url=beatmap.get('url'), color=color, timestamp=t ,description=desc)
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
    embed.set_image(url=beatmapset['covers'].get('cover'))
    embed.set_author(name=f"{user.get('username')}: {user_stats.get('pp')}pp (#{user_stats.get('global_rank'):,} {user.get('country_code')}{user_stats.get('country_rank'):,})", url=f"https://osu.ppy.sh/users/{str(user.get('id'))}",
                     icon_url=user.get('avatar_url'))
    embed.add_field(name="Grade", value=f"{emote_rank} {'+' if mods != [] else ''}{''.join(mods)}")
    embed.add_field(name="Score", value=f"{score.get('score'):,}")
    embed.add_field(name="Acc", value=f"{round(accuracy, 2)}%")
    embed.add_field(name="PP", value=f"**{round(result[0].pp, 2)}**/{round(result[2].pp, 2)}")
    embed.add_field(name="Combo", value=f"**{int(score.get('max_combo'))}x**/{result[2].maxCombo}x")
    embed.add_field(name="Hits", value=f"{{{int(stats.get('count_300'))}/{int(stats.get('count_100'))}/{int(stats.get('count_50'))}/{int(stats.get('count_miss'))}}}")
    embed.add_field(name="If FC: PP", value=f"**{round(result[1].pp, 2)}**/{round(result[2].pp, 2)}")
    embed.add_field(name="Acc", value=f"{round(accuracy, 2)}%")
    embed.add_field(name="Hits", value=f"{{{int(stats.get('count_300'))}/{int(stats.get('count_100'))}/{int(stats.get('count_50'))}/0}}")
    
    # ☆☆☆
    length = str(time.strftime('%M:%S', time.gmtime(int(beatmap.get("total_length")))))
    stars = beatmap.get('difficulty_rating')
    embed.add_field(name=f"**Maps Info**", value=f"length: `{length}` (`0:00`) BPM: `{beatmap.get('bpm')}` Objects: `{beatmap.get('count_circles') + beatmap.get('count_sliders') + beatmap.get('count_spinners')}` \nCS: `{beatmap.get('cs')}` AR: `{beatmap.get('ar')}` OD: `{beatmap.get('accuracy')}` HP: `{beatmap.get('drain')}` Stars: `{beatmap.get('difficulty_rating')}`", inline=False)
    embed.set_footer(text=f"{beatmap.get('status').capitalize()} map by {beatmapset.get('creator')} - (Bathbot version)")
    
    return embed


# ============================= #
#                               #
#              owo!             #
# osu!std only                  #
# ============================= #
def generate_embed_score_5(score, kind: str = "", color: int = 0xff66aa):

    beatmap = score.get('beatmap')
    # possiblement pas de beatmapset
    beatmapset = score.get('beatmapset')
    if beatmapset is None:
        beatmapset = OsuAPIv3.API().get_beatmapset(beatmap.get('beatmapset_id'))


    stats = score.get('statistics')

    mods = score.get('mods')
    if mods == None:
        mods = ["NM"]
    
    # ☆☆☆
    emote_rank = emotes.get(score.get("rank"))
    accuracy = score.get('accuracy') * 100
    user = score['user']
    user_stats = OsuAPIv3.API().get_user(user=user.get('id'))["statistics"]
    
    open("temp.osu", "wb" ).write(requests.get(f"https://osu.ppy.sh/osu/{beatmap.get('id')}").content)
    calculator = rosu_pp_py.Calculator("temp.osu")
    
    ParamNormal = rosu_pp_py.ScoreParams(acc=accuracy, mods=sum([Mods[k].value for k in mods]), n300=stats.get('count_300'), n100=stats.get('count_100'), n50=stats.get('count_50'), nMisses=stats.get('count_miss'), nKatu=stats.get('count_katu'), combo=score.get("max_combo"), score=score.get('score'))
    ParamFC = rosu_pp_py.ScoreParams(acc=accuracy, mods=sum([Mods[k].value for k in mods]))
    
    result = calculator.calculate([ParamNormal, ParamFC])
    print(result[0])
    
    t = datetime.datetime.strptime(score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")
    t = round(datetime.datetime.timestamp(t))
    best_scores = OsuAPIv3.API().get_user_score(user=user.get('id'), score_type="best", offset="20", limit=150, mode=score.get('mode'))
    desc = ""
    a = 0
    for s in best_scores:
        a += 1
        if score.get('best_id') == s.get('id'):
            desc = str(a)

    embed = discord.Embed(color=color,
                          description=f"{desc}{'.' if desc != '' else ''} {emote_rank} [{beatmapset.get('title')} [{beatmap.get('version')}]]({beatmap.get('url')}) {'+' if mods != [] else ''}{''.join(mods)} [{float(beatmap.get('difficulty_rating'))}★]"
                                      f"\n{score.get('score'):,} ◦ {round(accuracy, 2)}% ◦ {round(result[0].pp, 2)}pp  "
                                      f"\n**x{int(score.get('max_combo'))}**/{result[1].maxCombo} ◦ `[{int(stats.get('count_300'))} ● {int(stats.get('count_100'))} ● {int(stats.get('count_50'))} ● {int(stats.get('count_miss'))}]` <t:{t}:R>")
    
    embed.set_thumbnail(url=beatmapset['covers'].get('list'))
    embed.set_author(name=f"{user.get('username')}: {user_stats.get('pp')}pp ⇨ #{user_stats.get('global_rank'):,} ({{server}})", url=f"https://osu.ppy.sh/users/{str(user.get('id'))}", icon_url=score['user'].get('avatar_url'))
    embed.set_footer(text="(gurabot version)")
    
    return embed


def get_binded(discord_id: int = 0, osu_id: int = 0):
    if discord_id != 0:
        for p in data_p:
            if str(discord_id) == str(data_p[p]["discord_id"]):
                return data_p[p]
    else:
         for p in data_p:
            if str(osu_id) == str(data_p[p]["osu_id"]):
                return data_p[p]
    return None


class Mods(enum.IntFlag):
    NM = 0
    NF = 1
    EZ = 2
    HD = 8
    HR = 16
    SD = 32
    DT = 64
    RL = 128
    HT = 256
    NC = 512  # Only set along with DoubleTime. i.e: NC only gives 576
    FL = 1024
    AT = 2048
    SO = 4096
    AP = 8192  # Autopilot
    PF = 16384  # Only set along with SuddenDeath. i.e: PF only gives 16416  
    FI = 1048576
    RD = 2097152
    CM = 4194304
    TP = 8388608
    CP = 33554432
    SV2= 536870912
    MR = 1073741824
    FreeModAllowed = NF | EZ | HD | HR | SD | FL | FI | RL | AP | SO
    ScoreIncreaseMods = HD | HR | DT | FL | FI