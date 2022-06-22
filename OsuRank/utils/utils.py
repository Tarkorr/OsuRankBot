import datetime
import json
import time
import discord
import requests
import rosu_pp_py
import enum
from pprint import pprint
from . import OsuAPIv3


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
class generate_embed_score:
    
    def __init__(self, score, kind: str = "", color: int = 0xff66aa):
        
        self.score = score
        self.kind = kind
        self.color = color
        self.beatmap = score.get('beatmap')
        
        # possiblement pas de beatmapset
        self.beatmapset = score.get('beatmapset')
        if self.beatmapset is None:
            self.beatmapset = OsuAPIv3.API().get_beatmapset(self.beatmap.get('beatmapset_id'))
        
        # Beatmapset Data
        self.artist = self.beatmapset.get('artist')
        self.title = self.beatmapset.get('title')
        self.creator = self.beatmapset.get('creator')
        self.cover_card = self.beatmapset['covers'].get('card')
        self.cover_list = self.beatmapset['covers'].get('list')
        self.cover_cover = self.beatmapset['covers'].get('cover')
        self.beatmapset_id = self.beatmapset.get('id')
        
        # Beatmap Data
        self.total_length = time.strftime('%M:%S', time.gmtime(int(self.beatmap.get("total_length"))))
        self.stars = self.beatmap.get('difficulty_rating')
        self.bpm = float(self.beatmap.get('bpm'))
        self.objects = self.beatmap.get('count_circles') + self.beatmap.get('count_sliders') + self.beatmap.get('count_spinners')
        self.OD = self.beatmap.get('accuracy')
        self.AR = self.beatmap.get('ar')
        self.CS = self.beatmap.get('cs')
        self.HP = self.beatmap.get('drain')
        self.version = self.beatmap.get('version')
        self.status = self.beatmap.get('status')
        self.beatmap_id = self.beatmap.get('id')
        self.beatmap_url = self.beatmap.get('url')
        
        # user data
        self.user = score.get('user')
        self.user_id = self.user.get('id')
        self.user_stats = OsuAPIv3.API().get_user(user=self.user_id)["statistics"]
        self.mode = score.get("mode")
        self.img_mode = self.get_img_mode(self.mode)
        self.username = self.user.get('username')
        self.avatar_url = self.user.get('avatar_url')
        
        # score data
        self.created_at = datetime.datetime.strptime(self.score.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")
        self.stats = score.get('statistics')
        self.emote_rank = emotes.get(self.score.get("rank"))
        self.mods = score.get('mods')
        if self.mods == []:
            self.mods = ["NM"]
        self.total_score = score.get('score')
        self.count_300  = int(self.stats.get('count_300'))
        self.count_geki = int(self.stats.get('count_geki'))
        self.count_100  = int(self.stats.get('count_100'))
        self.count_katu = int(self.stats.get('count_katu'))
        self.count_50   = int(self.stats.get('count_50'))
        self.count_miss = int(self.stats.get('count_miss'))
        self.accuracy = score.get('accuracy') * 100
        self.combo = int(self.score.get('max_combo'))
        self.pos = self.pb_pos(self.user_id, self.mode, score.get('id'))
        
        # pp calculation + maxCombo (rosu_pp_py)
        open("temp.osu", "wb" ).write(requests.get(f"https://osu.ppy.sh/osu/{self.beatmap_id}").content)
        calculator = rosu_pp_py.Calculator("temp.osu")
        ParamNormal = rosu_pp_py.ScoreParams(acc=self.accuracy, mods=sum([Mods[k].value for k in self.mods]), n300=self.count_300, n100=self.count_100, n50=self.count_50, nMisses=self.count_miss, nKatu=self.count_katu, combo=score.get("max_combo"), score=score.get('score'))
        ParamFC = rosu_pp_py.ScoreParams(mods=sum([Mods[k].value for k in self.mods]), n300=self.count_300, n100=self.count_100, n50=self.count_50, nMisses=0)
        ParamBEST = rosu_pp_py.ScoreParams(mods=sum([Mods[k].value for k in self.mods]))
        
        self.result = calculator.calculate([ParamNormal, ParamFC, ParamBEST])    
        
        
        print(f"{self.username} completed the map {self.title}")


    def basic(self):
        # wprint(f"{username} completed the map {title}")

        embed = discord.Embed(title=f"**{self.title}**", url=self.beatmap_url, color=self.color, timestamp=self.created_at)
        embed.set_thumbnail(url=self.img_mode)
        embed.set_image(url=self.cover_card)
        embed.set_author(name=f"{self.status} completed by {self.username}", url=f"https://osu.ppy.sh/users/{self.user_id}", icon_url=self.avatar_url)
        # ☆☆☆
        embed.add_field(name = " __Beatmap informations:__ ", 
                        value = f"\n **__Durée:__** `{self.total_length}` "
                                f"\n **__stars:__** `{self.stars}☆`",
                        inline=False)
    
    
        embed.add_field(name = f"**__{self.kind}Score:__**", 
                        value = f"__rank:__{self.emote_rank}"
                                f"\n| `{self.count_300:03d}` {str(emotes.get('300'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_geki:03d}` {str(emotes.get('300g'))} |\n"
                                f"| `{self.count_100:03d}` {str(emotes.get('100'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_katu:03d}` {str(emotes.get('100k'))} |\n"
                                f"| `{self.count_50:03d}` {str(emotes.get('50'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_miss:03d}` {str(emotes.get('0'))} |"
                                f"\n| __pp:__ `{(round(self.result[0].pp)):03d}` pp |- - - - - - - - - - - -| "
                                f"__Mods:__ `{', '.join(self.mods)}`"
                                f"\n| __combo:__ `{self.combo:04d}` x |- - - - - - - - -|"
                                f"__Accuracy:__ `{round(self.accuracy, 2)} %`",
                        inline=True)

        return embed

    # ============================= #
    #                               #
    #          AIKA v1.1.5          #
    #                               #
    # ============================= #
    def aika(self):
        
        embed = discord.Embed(title=f"**{self.artist} - {self.title} \n[{self.version}]**",url=self.beatmap_url,
                            color=self.color,timestamp=self.created_at)
        

        embed.set_thumbnail(url=self.get_img_mode(self.mode))
        embed.set_image(url=self.cover_card)
        embed.set_author(name = f"[☆] {self.username} {self.kind} osu!{self.mode} play.", 
                         url=f"https://osu.ppy.sh/users/{self.user_id}", 
                         icon_url=self.avatar_url)
        
        # ☆☆☆
        embed.add_field(name = "Score informations", 
                        value = f" ▸  {self.emote_rank} **{round(self.accuracy, 2)}% {round(self.result[0].pp, 2)}pp** +{', '.join(self.mods)} {self.combo}/{self.result[0].maxCombo}x"
                                f"\n ▸ {{ {self.count_100}x100, {self.count_50}x50, {self.count_miss}xM }} ", 
                        inline=False)

        embed.add_field(name = "Beatmap informations", 
                        value = f"**{self.status.capitalize()} ⭐ {self.stars} | {self.total_length} @ 🎵 {self.bpm}**"
                                f"\n**AR** {self.AR} **OD** {self.OD} **[[Download](http://megumin.free.fr/ok/fumo.jpg)]**",
                        inline=False)
        
        embed.set_footer(text="(Aika version)")
        
        return embed


    # ============================= #
    #                               #
    #              owo!             #
    # osu!std only                  #
    # ============================= #
    def owo(self):
        
        # ☆☆☆
        embed = discord.Embed(color=self.color, timestamp=self.created_at, 
                            description=f" ► {self.emote_rank} ▸ **{round(self.result[0].pp, 2)}pp** ({round(self.result[1].pp, 2)}pp for {round(self.accuracy, 2)}% FC) ▸ {round(self.accuracy, 2)}%"
                                        f"\n ► {self.total_score:,} ▸ x{self.combo}/{self.result[1].maxCombo} ▸ [{self.count_300}/{self.count_100}/{self.count_50}/{self.count_miss}]")
        
        embed.set_thumbnail(url=self.cover_list)
        embed.set_author(name=f"{self.title} [{self.version}]  + {', '.join(self.mods)} [{self.stars}★]", url=self.beatmap_url, icon_url=self.avatar_url)
        embed.set_footer(text="(owo! version)")
        
        return embed


    # ============================= #
    #                               #
    #           Bathbot!            #
    # osu!std only                  #
    # ============================= #
    def bathbot(self):

        embed = discord.Embed(title=f"**{self.artist} - {self.title} [{self.version}]**",url=self.beatmap_url, color=self.color, timestamp=self.created_at,
                              description=f"{' ► Personnal best #' if self.pos != '' else ''}{self.pos}")

        embed.set_thumbnail(url=self.img_mode)
        embed.set_image(url=self.cover_cover)
        embed.set_author(name=f"{self.username}: {self.user_stats.get('pp')}pp (#{self.user_stats.get('global_rank'):,} {self.user.get('country_code')}{self.user_stats.get('country_rank'):,})", url=f"https://osu.ppy.sh/users/{self.user_id}",
                        icon_url=self.avatar_url)
        embed.add_field(name="Grade", value=f"{self.emote_rank} {'+' if self.mods != [] else ''}{''.join(self.mods)}")
        embed.add_field(name="Score", value=f"{self.total_score:,}")
        embed.add_field(name="Acc", value=f"{round(self.accuracy, 2)}%")
        embed.add_field(name="PP", value=f"**{round(self.result[0].pp, 2)}**/{round(self.result[2].pp, 2)}")
        embed.add_field(name="Combo", value=f"**{self.combo}x**/{self.result[2].maxCombo}x")
        embed.add_field(name="Hits", value=f"{{{self.count_300}/{self.count_100}/{self.count_50}/{self.count_miss}}}")
        embed.add_field(name="If FC: PP", value=f"**{round(self.result[1].pp, 2)}**/{round(self.result[2].pp, 2)}")
        embed.add_field(name="Acc", value=f"{round(self.accuracy, 2)}%")
        embed.add_field(name="Hits", value=f"{{{self.count_300}/{self.count_100}/{self.count_50}/0}}")
        
        # ☆☆☆
        embed.add_field(name=f"**Maps Info**", value=f"length: `{self.total_length}` (`0:00`) BPM: `{self.bpm}` Objects: `{self.objects}` \nCS: `{self.CS}` AR: `{self.AR}` OD: `{self.OD}` HP: `{self.HP}` Stars: `{self.stars}`", inline=False)
        embed.set_footer(text=f"{self.status.capitalize()} map by {self.creator} - (Bathbot version)")
        
        return embed


    # ============================= #
    #                               #
    #             gura              #
    # osu!std only                  #
    # ============================= #
    def gurabot(self):
        
        # ☆☆☆
        embed = discord.Embed(color=self.color,
                            description=f"{self.pos}{'.' if self.pos != '' else ''} {self.emote_rank} [{self.title} [{self.version}]]({self.beatmap_url}) {'+' if self.mods != [] else ''}{'|'.join(self.mods)} [{self.stars}★]"
                                        f"\n{self.total_score:,} ◦ {round(self.accuracy, 2)}% ◦ {round(self.result[0].pp, 2)}pp"
                                        f"\n**x{self.combo}**/{self.result[1].maxCombo} ◦ `[{self.count_300} ● {self.count_100} ● {self.count_50} ● {self.count_miss}]` <t:{round(datetime.datetime.timestamp(self.created_at))}:R>")
        
        embed.set_thumbnail(url=self.cover_list)
        embed.set_author(name=f"{self.username}: {self.user_stats.get('pp')}pp ⇨ #{self.user_stats.get('global_rank'):,} ({{server}})", url=f"https://osu.ppy.sh/users/{self.user_id}", icon_url=self.avatar_url)
        embed.set_footer(text="(gurabot version)")
        
        return embed
    
    
    def pb_pos(self, user, mode, score_id):
        d = ""
        a = 0
        best_scores = OsuAPIv3.API().get_user_score(user=user, score_type="best", limit=100, mode=mode)
        for s in best_scores:
            a += 1
            if score_id == s.get('id'):
                d = str(a)
        return d
    
    
    def get_img_mode(self, mode):
        
        # img_osu: "https://i.imgur.com/bnSSOS9.png"
        # img_mania: "https://i.imgur.com/NVkykfe.png"
        # img_taiko: "https://i.imgur.com/iSQFSTn.png"
        # img_ctb: "https://i.imgur.com/MjOv5Kd.png"
        
        if mode == "mania":
            return "https://i.imgur.com/NVkykfe.png"
        elif mode == "osu":
            return "https://i.imgur.com/bnSSOS9.png"
        elif mode == "fruits":
            return "https://i.imgur.com/MjOv5Kd.png"
        else:
            return "https://i.imgur.com/iSQFSTn.png"


def get_binded(discord_id: int = 0, osu_id: int = 0):
    data_p = json.loads(open('players.json', "r").read())
    if discord_id != 0:
        for p in data_p:
            if str(discord_id) == str(data_p[p]["discord_id"]):
                return data_p[p]
    else:
         for p in data_p:
            if str(osu_id) == str(data_p[p]["osu_id"]):
                return data_p[p]
    data_p.close()
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