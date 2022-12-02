import datetime
import json
import time
import discord
import requests
import rosu_pp_py
import typing
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
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

    "0": "<:hit0:1030911650200551455>",
    "50": "<:hit50:1030911651882479626>",
    "100": "<:hit100:1030911653002346538>",
    "100k": "<:hit100k:1030911654650720437>",
    "300": "<:hit300:1030911655468597340>",
    "300g": "<:hit300g:1030911657960013864>",
    "300k": "<:hit300k:1030911649185546250>",

    "Arrow": "<:arrow:1030914480244281505>",
    "On": "<:status_online:887380229985820732>",
    "Off": "<:status_offline:887380229713182741>",
    "WasSupporter": "<:hasSupporter:1030918359635730463>",
    "Supporter": "<:supporter:1030918358020927609>"
}
class generate_embed_score:
    
    def __init__(self, score, kind: str = "", color: int = 0xff66aa):
        # print('pass 0.5')
        self.API = OsuAPIv3.API()
        self.score = score
        self.kind = kind
        self.color = color
        
        self.server = self.score.get('server')
        if self.score.get('server') != None: # Le server n'est as bancho
            self.score['beatmap'] = self.API.get_beatmap(self.score.get('beatmap_id'))
        # Beatmap Data
        # print('pass 1')
        self.beatmap = score.get('beatmap')
        
        # possiblement pas de beatmapset
        # print('pass 2')
        self.beatmapset = score.get('beatmapset')
        if self.beatmapset is None:
            self.beatmapset = self.API.get_beatmapset(self.beatmap.get('beatmapset_id'))
        
        # Beatmapset Data
        # print('pass 3')
        self.artist = self.beatmapset.get('artist')
        self.title = self.beatmapset.get('title')
        self.creator = self.beatmapset.get('creator')
        self.cover_card = self.beatmapset['covers'].get('card')
        self.cover_list = self.beatmapset['covers'].get('list')
        self.cover_cover = self.beatmapset['covers'].get('cover')
        self.beatmapset_id = self.beatmapset.get('id')
        
        # Beatmap Data
        # print('pass 4')
        self.total_length = time.strftime('%M:%S', time.gmtime(int(self.beatmap.get("total_length"))))
        self.hit_length = time.strftime('%M:%S', time.gmtime(int(self.beatmap.get("hit_length"))))
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
        # print('pass 5')
        self.user = score.get('user')
        self.user_id = self.user.get('id')
        self.user_stats = self.API.get_user(user=self.user_id)["statistics"]
        self.mode = score.get("mode")
        self.mode_int = score.get("mode_int")
        self.img_mode = self.get_img_mode(self.mode)
        self.username = self.user.get('username')
        self.avatar_url = self.user.get('avatar_url')
        
        # score data
        # print('pass 6')
        self.created_at = datetime.datetime.strptime(self.score.get('created_at'), "%Y-%m-%dT%H:%M:%SZ") # old: "%Y-%m-%dT%H:%M:%S+00:00"
        self.stats = score.get('statistics')
        self.emote_rank = emotes.get(self.score.get("rank"))
        self.mods = score.get('mods')
        self.mods = ["NM"] if self.mods == [] else self.mods
        
        # print('pass 6.5')
        if self.mods is None:
            self.mods_int = self.score.get('mods_int')
        else:
            self.mods_int = sum([Mods[k].value for k in self.mods])
        # print('pass 6.6')
        self.total_score = score.get('score')
        self.FC = self.score.get("perfect")
        self.count_300  = int(self.stats.get('count_300'))
        self.count_geki = int(self.stats.get('count_geki'))
        self.count_100  = int(self.stats.get('count_100'))
        self.count_katu = int(self.stats.get('count_katu'))
        self.count_50   = int(self.stats.get('count_50'))
        self.count_miss = int(self.stats.get('count_miss'))
        self.accuracy = score.get('accuracy') * 100
        self.combo = int(self.score.get('max_combo'))
        if self.score.get('server') == None:
            self.pos = self.pb_pos(self.user_id, self.mode, score.get('id'))
        else:
            self.pos = ''

        # print('pass 7')
        map_ = rosu_pp_py.Beatmap(bytes=requests.get(f"https://osu.ppy.sh/osu/{self.beatmap_id}").content)
        # available:  'mode', 'mods', 'n_geki', 'n_katu', 'n300', 'n100', 'n50', 'n_misses', 'acc', 'combo', 'passed_objects', 'clock_rate', or 'difficulty'
        ParamNormal = rosu_pp_py.Calculator(mode=self.mode_int, acc=self.accuracy, mods=self.mods_int, n300=self.count_300, n100=self.count_100, n50=self.count_50, n_geki=self.count_geki, n_katu=self.count_katu, n_misses=self.count_miss, combo=score.get("max_combo"))
        ParamFC = rosu_pp_py.Calculator(mode=self.mode_int, mods=self.mods_int, n300=self.count_300, n100=self.count_100, n50=self.count_50, n_geki=self.count_geki, n_katu=self.count_katu, n_misses=self.count_miss)
        ParamBEST = rosu_pp_py.Calculator(mode=self.mode_int, mods=self.mods_int)
        
        # question d'habitude ancienne version de rosu_pp_py utilisait un 'calculator', qui donnait une liste donc on reste sur une liste pour stock les résultats.
        # print('pass 8')
        self.result = [ParamNormal.performance(map_), ParamFC.performance(map_), ParamBEST.performance(map_)]
        self.pp_Normal = self.result[0].pp if self.result[0].pp != float('inf') else 1 # type: ignore + ahahahahhahah c'est illisible
        self.pp_FC = self.result[1].pp # type: ignore
        self.pp_BEST = self.result[2].pp # type: ignore
        
        if self.mode_int==0:
            self.max_combo = self.result[2].difficulty.max_combo # type: ignore
        else:
            self.max_combo = None
        
        print(f"{self.username} completed the map {self.title}" 
            f"\nEverything seems to be fine... For further research, acknowledge these facts:"
            f" pp: {round(self.pp_Normal)}/{round(self.pp_BEST)}pp combo: {self.combo}/{self.max_combo} acc: {round(self.accuracy, 2)}% stars: {self.stars}*") # type: ignore


    # ---------- #
    #  Basic v2  #
    # ---------- #
    def basic(self):
        # wprint(f"{username} completed the map {title}")

        embed = discord.Embed(title=f"**{self.title}**", url=self.beatmap_url, color=self.color, timestamp=self.created_at)
        embed.set_thumbnail(url=self.img_mode)
        embed.set_image(url=self.cover_card)
        embed.set_author(name=f"{self.status} completed by {self.username} on {self.server if self.server != None else 'bancho'}", url=f"https://osu.ppy.sh/users/{self.user_id}", icon_url=self.avatar_url)
        # ☆☆☆
        embed.add_field(name = " __Beatmap informations:__ ", 
                        value = f"\n **__Durée:__** **{self.hit_length}** [{self.total_length}]"
                                f"\n **__stars:__** **{self.stars}☆**",
                        inline=False)
    
        embed.add_field(name = f"**__{self.kind}Score:__**", 
                        value = f"__rank:__ {self.emote_rank} {'(**FC**)' if self.FC else '(**~FC**)' if self.max_combo == self.combo else ''}" # type: ignore
                                f"\n| `{self.count_300:03d}` {str(emotes.get('300'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_geki:03d}` {str(emotes.get('300g'))} |\n"
                                f"| `{self.count_100:03d}` {str(emotes.get('100'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_katu:03d}` {str(emotes.get('100k'))} |\n"
                                f"| `{self.count_50:03d}` {str(emotes.get('50'))} |- - - - - - - - - - - - - -| "
                                f"`{self.count_miss:03d}` {str(emotes.get('0'))} |"
                                f"\n| __pp:__ **{(round(self.pp_Normal, 2))}**/{(round(self.pp_BEST, 2))} | - ∙ - | " # type: ignore
                                f"__Mods:__ `{Mods(self.mods_int).__str__().strip('Mods.')}`"
                                f"\n| __combo:__ **{self.combo}**{f'/{self.max_combo}' if self.max_combo != None else ''}x | - ∙ - | " # type: ignore
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
                        value = f" ▸  {self.emote_rank} **{round(self.accuracy, 2)}% {round(self.pp_Normal, 2)}pp** +{', '.join(self.mods)} {self.combo}/{self.max_combo}x" # type: ignore
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
                            description=f" ► {self.emote_rank} ▸ **{round(self.pp_Normal, 2)}pp** ({round(self.pp_FC, 2)}pp for {round(self.accuracy, 2)}% FC) ▸ {round(self.accuracy, 2)}%" # type: ignore
                                        f"\n ► {self.total_score:,} ▸ x{self.combo}/{self.max_combo} ▸ [{self.count_300}/{self.count_100}/{self.count_50}/{self.count_miss}]") # type: ignore
        
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
        embed.add_field(name="PP", value=f"**{round(self.pp_Normal, 2)}**/{round(self.pp_BEST, 2)}") # type: ignore
        embed.add_field(name="Combo", value=f"**{self.combo}x**/{self.max_combo}x") # type: ignore
        embed.add_field(name="Hits", value=f"{{{self.count_300}/{self.count_100}/{self.count_50}/{self.count_miss}}}")
        embed.add_field(name="If FC: PP", value=f"**{round(self.pp_FC, 2)}**/{round(self.pp_BEST, 2)}") # type: ignore
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
                                        f"\n{self.total_score:,} ◦ {round(self.accuracy, 2)}% ◦ {round(self.pp_Normal, 2)}pp" # type: ignore
                                        f"\n**x{self.combo}**/{self.max_combo} ◦ `[{self.count_300} ● {self.count_100} ● {self.count_50} ● {self.count_miss}]` <t:{round(datetime.datetime.timestamp(self.created_at))}:R>") # type: ignore
        
        embed.set_thumbnail(url=self.cover_list)
        embed.set_author(name=f"{self.username}: {self.user_stats.get('pp')}pp ⇨ #{self.user_stats.get('global_rank'):,} ({{server}})", url=f"https://osu.ppy.sh/users/{self.user_id}", icon_url=self.avatar_url)
        embed.set_footer(text="(gurabot version)")
        
        return embed
    
    
    def pb_pos(self, user, mode, score_id):
        d = ""
        a = 0
        best_scores = self.API.get_user_score(user=user, score_type="best", limit=100, mode=mode)
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
        
    
    def calculate_acc(self, stats, mode):
        n300  = stats.get('count_300')
        n300g = stats.get('count_geki')
        n100  = stats.get('count_100')
        n100k = stats.get('count_katu')
        n50   = stats.get('count_50')
        nmiss    = stats.get('count_miss')
        if mode == 'osu':
            return (300*n300 + 100*n100 + 50*n50) / (300*(n300+n100+n50+nmiss))
        if mode == 'taiko':
            return (n100k + 0.5*n100) / (n100k + n100 + nmiss) # unsure
        if mode == 'fruits':
            return # TODO
        if mode == 'mania':
            return (50 * n50 + 100 * n100 + 200 * n100k + 300 * (n300 + n300g)) / (300 * (nmiss + n50 + n100 + n100k + n300 + n300g))


def get_binded(discord_id: int = 0, osu_id: int = 0):
    data_p = json.loads(open('players.json', "r").read())
    if discord_id != 0:
        for p in data_p:
            if str(discord_id) == str(data_p[p]["discord_id"]):
                return data_p[p]
        return None
    else:
        for p in data_p:
            if str(osu_id) == str(data_p[p]["osu_id"]):
                return data_p[p]
        return None

def get_courbe(rank_history: list):

    y = [a/1000 for a in rank_history]
    x = [a for a in range(len(y))]

    fig, ax = plt.subplots()
    ax.plot(x, y, "#5865F2", linewidth=4)
    ax.set_facecolor('#2C2F33') # 2C2F33
    ax.invert_yaxis()
    ax.get_xaxis().set_visible(False)
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:n}k'))
    ax.grid()

    fig.patch.set_facecolor('#23272A') # 23272A
    fig.set_figwidth(16)
    fig.set_figheight(4)

    plt.yticks(fontsize=16, color="w")
    plt.xlim([-1, max(x)+0.5])
    plt.rcParams["figure.autolayout"] = True
    plt.savefig('plot.png', transparent=False)
    return True


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