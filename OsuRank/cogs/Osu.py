import datetime
import os
import typing
import discord
import json
import requests
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from OsuRank.utils import OsuAPIv2, OsuAPI, utils
from OsuRank.utils import display_score as dp
from bs4 import BeautifulSoup

prefix = "!o "
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
osu_modes = ["mania", "osu", "fruits", "taiko"]

cfg = json.loads(open("config_OSU.json", "r").read())
class KEYS:
    OSU_API = cfg["OSU_API"]
    my_id = int(cfg["me"])
    token = cfg["token"]
    guild_id = cfg["server-id"]
    logs_channel = cfg["logs-channel-id"]


class Osu(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        emoji = reaction.emoji

        if user.bot:
            return

        if emoji == '🟦':
            if user.id != KEYS.my_id and user.display_name != message.embeds[0].footer.text:
                return
            # take the embed of the message
            embed = message.embeds[0]
            # take the first field
            f = embed.fields[0]

            val = f.value.replace(":white_large_square:", ":blue_square:", 1)
            embed.set_field_at(0, name=f.name, value=val, inline=True)
            await message.edit(embed=embed)
            await message.remove_reaction(emoji, user)
        elif emoji == '🟥':
            if user.id != KEYS.my_id and user.display_name != message.embeds[0].footer.text:
                return
            # take the embed of the message
            embed = message.embeds[0]
            # take the first field
            f = embed.fields[1]

            val = f.value.replace(":white_large_square:", ":red_square:", 1)
            embed.set_field_at(1, name=f.name, value=val, inline=True)
            await message.edit(embed=embed)
            await message.remove_reaction(emoji, user)
        elif emoji == '🔄':
            if user.id != KEYS.my_id and user.display_name != message.embeds[0].footer.text:
                return
            # take the embed of the message
            embed = message.embeds[0]
            # take fields
            field_1 = embed.fields[0]
            field_2 = embed.fields[1]

            # reset values
            value_1 = field_1.value.replace(":blue_square:", ":white_large_square:")
            value_2 = field_2.value.replace(":red_square:", ":white_large_square:")

            embed.set_field_at(0, name=field_1.name, value=value_1, inline=True)
            embed.set_field_at(1, name=field_2.name, value=value_2, inline=True)
            await message.edit(embed=embed)
            await message.remove_reaction(emoji, user)

        elif emoji == "🏆":
            embed = message.embeds[0]

            if "completed by" in embed.author.name:
                user_id = os.path.split(embed.author.url)[1]
                beatmap_id = os.path.split(embed.url)[1]

                play = OsuAPIv2.get_data_user_score(beatmap_id, user_id)["score"]
                await message.edit(embed=utils.generate_embed_score(play, "Best "))
                await message.remove_reaction(emoji, user)

        elif emoji == '⏰':
            embed = message.embeds[0]

            if "completed by" in embed.author.name:

                user_id = os.path.split(embed.author.url)[1]
                beatmap_id = os.path.split(embed.url)[1]

                mode = OsuAPIv2.get_data_user_score(beatmap_id, user_id)["score"]["mode"]
                recent_maps = OsuAPIv2.get_data_user_recent(user_id, mode)
                for beatmap in recent_maps:
                    if beatmap_id == str(beatmap["beatmap"]["id"]):
                        await message.edit(embed=utils.generate_embed_score(beatmap, "Last "))
                        await message.remove_reaction(emoji, user)
                        return
                embed.set_field_at(1, name="**__Fail:__**",
                                value=f"Le joueur n'a pas de score récent durant les dernières 24h"
                                        f" ou il a envoyé 5 scores ou plus sur des maps différentes."
                                        f"Donc pas de données récente sur la map.",
                                inline=True)
                await message.edit(embed=embed)
                await message.remove_reaction(emoji, user)
        else:
            return

    
    @commands.command(name="display_score",
             aliases=["dp"],
             usage=f"{prefix}display_score <user> <mode>",
             brief="affiche le score de <user> et son <mode>, //TODO"
             )
    async def display_score(self, ctx, USER, MODE: str = "0"):
        print(f"commande 'display_score' éxécuté par {ctx.author}")
        return await ctx.send("maybe...")
        last_game = check_last_game(USER, MODE)
        last_game = last_game['beatmap_id']
        if MODE == "3":
            score_data = OsuAPI.get_data_user_score(last_game, USER, MODE)
            map_data = OsuAPI.get_data_beatmap(last_game, MODE)
            # print("map_data = " + str(map_data))
            # print("score_data =" + str(score_data))
            # need to check last score
            marvelous = int(score_data[0]['countgeki'])
            perfect = int(score_data[0]['count300'])
            great = int(score_data[0]['countkatu'])
            good = int(score_data[0]['count100'])
            bad = int(score_data[0]['count50'])
            miss = int(score_data[0]['countmiss'])
            maxcombo = int(score_data[0]['maxcombo'])
            total_score = int(score_data[0]['score'])
            rank = score_data[0]['rank']

            url = "https://assets.ppy.sh/beatmaps/" + map_data[0]['beatmapset_id'] + "/covers/cover.jpg"
            r = requests.get(url)
            with open("cover.jpg", "wb") as f:
                f.write(r.content)

            accuracy = round(((50 * bad + 100 * good + 200 * great + 300 * (perfect + marvelous)) /
                            (300 * (miss + bad + good + great + perfect + marvelous)) * 100), 2)
            print("accuracy = " + str(accuracy))
            dp.main(total_score=str(total_score), scoreM=str(marvelous), scoreP=str(perfect), scoreGreat=str(great),
                    scoreGood=str(good), scoreB=str(bad), scoreMiss=str(miss), accuracy=str(accuracy),
                    maxcombo=str(maxcombo), rank=str(rank))
            await ctx.send(f"wip", file=discord.File("panel.png"))

        else:
            await ctx.send(f"not made yet", file=discord.File("error.jpg"))
        

    @commands.command(name="search",
             aliases=[],
             usage=f"{prefix}search <query> <mode>",
             brief="recherche quelque chose sur osu!, //todo"
             )
    async def search(self, ctx, query, mode: str = ""):
        print(f"commande 'info' éxécuté par {ctx.author}")
        data = OsuAPIv2.search(query, mode)
        users = []
        data = data.get('user').get('data')
        print(data)
        for i in range(len(data)):
            users.append(data[i].get("username"))
        gamers = ' \n'.join(users)
        await ctx.send(f" first {len(data)} founds, users names : \n{gamers}")
    

    @commands.command(name="last_play",
             aliases=["lp"],
             usage=f"{prefix}last_play <user> <mode>",
             brief="affiche le dernier score de <user>."
             )
    async def last_play(self, ctx,
                        user: str = "",
                        mode: str = "osu"):

        bme = ["<", "@", ">"]
        if any(x in user for x in bme):
            user_discord_id = user
            for b in bme:
                if b in user_discord_id:
                    user_discord_id = user_discord_id.replace(b, "")
            
            for p in data_p:
                if str(user_discord_id) == str(data_p[p]["discord_id"]):
                    user = str(data_p[p]["osu_id"])
                    mode = str(data_p[p]["mode"])
                    break
            else:
                return await ctx.send("La personne que tu as ping n'est pas lié avec le bot"
                                    "\nFais `!o bind <url profil osu>` pour bind ton profil osu.")
            

        if user == "":
            for p in data_p:
                if str(ctx.author.id) == str(data_p[p]["discord_id"]):
                    user = str(data_p[p]["osu_id"])
                    mode = str(data_p[p]["mode"])
                    break
            else:
                return await ctx.send("Tu peux mettre un pseudo ?"
                                    "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")

        # fetch data of user
        data_m = OsuAPIv2.get_data_user(user_id=user, mode=mode)

        if data_m == "404":
            # relou, parce que quand on le fait pour soit même bah ça mets l'id
            return await ctx.send(f"erreur {user} n'éxiste pas.")

        if mode == '':
            mode = data_m['playmode']

        elif mode not in osu_modes:
            # aucune verification de si MODE existe vraiment pas fou ngl.
            # j'ai écris le commentaire au dessus je sais pas quand du coup je comprends pas :/
            # j'ai compris hihi
            return await ctx.send(f"bah {mode} n'est pas un mode.")

        user_id = str(data_m['id'])
        username = data_m['username']

        play = OsuAPIv2.get_data_user_recent(user_id=user_id, mode=mode)

        if not play:
            return await ctx.send(f"{username} n'a pas de parties récentes.")
        else:
            play = play[0]

        rank_embed = await ctx.send(embed=utils.generate_embed_score(play, "Last "))
        emojis = ['🏆', '⏰']
        for emoji in emojis:
            await rank_embed.add_reaction(emoji)
    

    @commands.command(name="rank",
             aliases=[],
             usage=f"{prefix}rank <user> <mode>",
             brief="affiche sur une petite carte le rank de <user>."
             )
    async def rank(self, ctx, USER: str = "", MODE: typing.Optional[str] = "osu"):
        # amount: typing.Optional[int] = 99
        print(f"commande 'NeverForget' éxécuté par {ctx.author}")

        if USER == "":
            for p in data_p:
                if str(ctx.author.id) == str(data_p[p]["discord_id"]):
                    USER = str(data_p[p]["osu_id"])
                    break
            else:
                await ctx.send("Tu peux mettre un pseudo ?")
                return

        data_m = OsuAPIv2.get_data_user(user_id=USER, mode=MODE)
        if data_m == "404":
            return await ctx.send(f"mmmh ? {USER} n'a jamais joué à osu!")

        baseImage = Image.open("cards/card_osu_V1.png")

        if ctx.author == self.client.get_user(KEYS.my_id):
            await ctx.send("Bonjour Maître.")
            baseImage = Image.open("cards/card_Tarkor.png")
        if ctx.author == self.client.get_user(566879332606410752):
            baseImage = Image.open("cards/cardSacha.png")
        if ctx.author == self.client.get_user(455285319831519234):
            baseImage = Image.open("cards/cardFayber.png")

        # store data
        username = str(data_m["username"])
        pp_rank = str(data_m["statistics"]["global_rank"])
        level = str(data_m["statistics"]["level"]["current"])
        pp_raw = str(data_m["statistics"]["pp"])

        # create custom card
        color = (192, 48, 113, 255)
        image_editable = ImageDraw.Draw(baseImage)

        # username
        Username_pos = (30, 30)
        Username_font = "cards/Ubuntu.ttf"
        Username_font = ImageFont.truetype(Username_font, 50)
        image_editable.text(Username_pos, username, fill=color, font=Username_font)

        # level
        level_pos = (185, 108)
        level_font = "cards/Ubuntu.ttf"
        level_font = ImageFont.truetype(level_font, 43)
        image_editable.text(level_pos, str(round(float(level))), fill=color, font=level_font)

        # rank
        Rank_pos = (570, 35)
        Rank_font = "cards/Ubuntu.ttf"
        Rank_font = ImageFont.truetype(Rank_font, 40)
        image_editable.text(Rank_pos, pp_rank, fill=color, font=Rank_font)

        # pp
        pp_pos = (387, 112)
        pp_font = "cards/Ubuntu.ttf"
        pp_font = ImageFont.truetype(pp_font, 40)
        image_editable.text(pp_pos, str(round(float(pp_raw))), fill=color, font=pp_font)

        baseImage.save("cards/card.png")
        await ctx.send(file=discord.File("cards/card.png"))
    

    @commands.command(name="bind",
             aliases=[],
             usage=f"{prefix}bind <url> ",
             brief="permet de stoquer les infos d'un joueur en local, pour faciliter certaines commandes."
             )
    async def bind(self, ctx, url: str = "", params: str = ""):
        print(f"commande 'bind' éxécuté par {ctx.author}")

        if ctx.author.id == KEYS.my_id:
            if params == "remove":
                if url not in data_p:
                    await ctx.send(f"**{url}** n'y est pas.")
                    return
                del data_p[url]
                json.dump(data_p, open('players.json', 'w'))
                await ctx.send(f"**{url}** a été retiré.")
                return

            if params == "list":
                await ctx.send(" la resp list contient :  " + str(data_p))
                return

        if url == "":
            await ctx.send("url manquant.")
        else:
            me = self.client.get_user(KEYS.my_id)

            osu_id = os.path.split(url)[1]
            discord_id = ctx.author.id

            data_o = OsuAPIv2.get_data_user(user_id=osu_id)

            username = data_o['username']
            playmode = data_o['playmode']
            pp = data_o['statistics']['pp']
            rank = data_o['statistics']['global_rank']

            for p in data_p:
                if str(discord_id) == str(data_p[p]["discord_id"]):
                    await ctx.send(f"l'id `{discord_id}` est déjà enregistré,"
                                f"\nbind avec : __{data_p[p]['username']}__ ({data_p[p]['osu_id']})"
                                f"\nen cas de problème dm **{me}**")
                    return
                elif osu_id == str(data_p[p]["osu_id"]):
                    await ctx.send(f"l'id `{osu_id}` est déjà enregistré,"
                                f"\nbind avec : __{data_p[p]['username']}__"
                                f"\nen cas de problème dm **{me}**")
                    return

            await me.send(f"=" * 50 +
                        f"\n**{ctx.author}** said he was **{username}** ({playmode}). "
                        f"\n**__rank:__** `{rank}`."
                        f"\n**__with:__** `{pp}`pp.\n" +
                        f"=" * 50)

            new_user = {
                username: {
                    "discord_id": discord_id,
                    "osu_id": osu_id,
                    "color": "0x1f1e33",
                    "username": username,
                    "mode": playmode
                }
            }

            data_p.update(new_user)
            json.dump(data_p, open("players.json", "w"))
            await ctx.send("**" + username + "**" + " a été ajouté")
    

    @commands.command(name="score",
             aliases=[],
             usage=f"{prefix}score <url> <user> <mode>",
             brief="affiche un score spécifique."
             )
    async def score(self, ctx,
                    url: str = "",
                    user: str = "",
                    mode: str = "osu"):
        print(f"commande 'score' éxécuté par {ctx.author}")
        if user == "":
            if type(utils.get_binded(ctx.author.id)) == tuple:
                username, user_id, mode, color = utils.get_binded(ctx.author.id)
            else:
                await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
                return

        data_m = OsuAPIv2.get_data_user(user_id=user, mode=mode)
        if data_m == "404":
            # relou, parce que quand on le fait pour soit même bah ça mets l'id
            return await ctx.send(f"mmmh ? {user} n'a jamais joué à osu!")

        if mode == '':
            mode = data_m['playmode']
        else:
            # aucune verification de si MODE existe vraiment pas fou ngl.
            # j'ai écris le commentaire au dessus je sais pas quand du coup je comprends pas :/
            mode = mode
        user_id = str(data_m['id'])
        map_id = os.path.split(url)[1]

        play = OsuAPIv2.get_data_user_score(user_id=user_id, map_id=map_id, mode=mode)['score']
        rank_embed = await ctx.send(embed=utils.generate_embed_score(play))
        emojis = ['🏆', '⏰']
        for emoji in emojis:
            await rank_embed.add_reaction(emoji)


    @commands.command(name="top_scores",
                aliases=["ts"],
                usage=f"{prefix}top_scores <user> <mode> <limit>",
                brief="affiche les meilleurs scores."
                )
    async def top_scores(self, ctx,
                        username: str = "",
                        mode: str = "osu",
                        limit: int = 5):
        print(f"commande 'top_scores' éxécuté par {ctx.author}")

        if username == "":
            if type(utils.get_binded(ctx.author.id)) == tuple:
                username, user_id, mode, color = utils.get_binded(ctx.author.id)
            else:
                await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
                return
        else:
            color = 0xff69b4
            data_o = OsuAPIv2.get_data_user(user_id=username, mode=mode)

            if data_o == "404":
                return await ctx.send(f"mmmh ? {username} n'a jamais joué à osu!")
            user_id = data_o['id']

        data_m = OsuAPIv2.get_data_user_best(user_id=user_id, mode=mode, limit=limit)

        embed = discord.Embed(color=color, title=f"Meilleurs scores de {username}")
        for result in data_m:
            beatmap = result.get("beatmap")
            beatmapset = result.get("beatmapset")
            stats = result.get("statistics")
            emote_rank = emotes.get(result.get("rank"))
            t = datetime.datetime.strptime(result.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")
            t = round(datetime.datetime.timestamp(t))

            if not result.get('mods'):
                mods = "No Mod"
            else:
                mods = ', '.join(result.get('mods'))

            if result.get('perfect'):
                FC = ":white_check_mark:"
            else:
                FC = ":x:"

            embed.add_field(
                name=f"{beatmapset.get('title')} par {beatmapset.get('creator')}",
                value=f"`{beatmap.get('difficulty_rating')}`☆ | "
                    f"**OD**: {beatmap.get('accuracy')} | "
                    f"**AR**: {beatmap.get('ar')} | "
                    f"**CS**: {beatmap.get('cs')} | "
                    f"**HP**: {beatmap.get('drain')} | "
                    f"**BPM**: {beatmap.get('bpm')}"
                    f"\n**Accuracy:** `{round(result.get('accuracy') * 100, 1)}`% |- - - - - - - - - - - - - - -|"
                    f" **pp:** `{round(result.get('pp'), 2)}`pp"
                    f"\n**rank:**{emote_rank} |- - - - - - - - - - - - - - - - - - - - - -|"
                    f" **Mods:**`{mods}`"
                    f"\n**FC:**  {FC} |- - - - - - - - - - - - - - - - - - - - - - -|"
                    f" **date**: <t:{t}:R>",
                inline=False
            )
        await ctx.send(embed=embed)


    @commands.command(name="classement",
                aliases=["c"],
                usage=f"{prefix}classement <type>",
                brief="classement De OSUS, pour être dedans `!o bind <profil_url>`."
                )
    async def classement(self, ctx, type: str = ""):
        print(f"commande 'classement' éxécuté par {ctx.author}")
        embed = discord.Embed(title="Classement des Joueurs Osus.", color=0xff66aa, timestamp=datetime.datetime.now())
        embed.add_field(name="Fetching data.", value="Check...")
        message = await ctx.send(embed=embed)
        classement_types = ["pp", "rank", "playcount", "accuracy"]
        units = ["Joe Mama", "pp", "", "", "%"]
        blacklist = ["Tarkor"]

        if type not in classement_types:
            embed.set_field_at(0, name="No Type, No data.", value="Use a type :\n" + "\n".join(classement_types))
            return await message.edit(embed=embed)
        else:
            pattes = []
            compter = 0

            for p in data_p:
                embed.set_field_at(0,
                                value="can take some time... Wait... \n[" + str(round((compter / len(data_p)) * 100)) +
                                        "%]",
                                name=embed.fields[0].name)
                await message.edit(embed=embed)

                data_u = OsuAPIv2.get_data_user(data_p[p]["osu_id"])
                stats = data_u.get('statistics')

                # 0: (Username, osu_id), 1: pp, 2: rank, 3: playcount, 4: acc
                if data_u.get('username') in blacklist:
                    data_u['username'] = f"{data_u['username']} (mania)"

                # patrick et pattes pour des raisons de manque d'inspi.
                patrick = ((data_u.get('username'), data_p[p]['osu_id']), round(stats.get('pp')),
                        stats.get('global_rank'), stats.get('play_count'),
                        round(stats.get('hit_accuracy'), 2))
                pattes.append(patrick)
                compter += 1

            embed.remove_field(0)

        # reverse
        if type == classement_types[1]:
            kind = 2
            edf = sorted(pattes, key=lambda student: student[kind])
            edf.reverse()
        # normal
        else:
            kind = classement_types.index(type) + 1
            edf = sorted(pattes, key=lambda student: student[kind])

        embed.add_field(name=f"__classement {type}__:",
                        value=f":first_place: **{edf[len(edf) - 1][0][0]}**: {edf[len(edf) - 1][kind]:,}{units[kind]}"
                            f"\n:second_place: **{edf[len(edf) - 2][0][0]}**: {edf[len(edf) - 2][kind]:,}{units[kind]}"
                            f"\n:third_place:** {edf[len(edf) - 3][0][0]}**: {edf[len(edf) - 3][kind]:,}{units[kind]}"
                            f"\n4: **{edf[len(edf) - 4][0][0]}**: {edf[len(edf) - 4][kind]:,}{units[kind]}"
                            f"\n5: **{edf[len(edf) - 5][0][0]}**: {edf[len(edf) - 5][kind]:,}{units[kind]}")
        embed.set_thumbnail(url=f"http://s.ppy.sh/a/{edf[len(edf) - 1][0][1]}")

        await message.edit(embed=embed)


    @commands.command(name="skill",
                aliases=["s"],
                usage=f"{prefix}skill <user>",
                brief="Obtient le skill d'un joueur scrap de https://osuskills.com/")
    async def skill(self, ctx, username: str = ""):
        print(f"commande 'skill' éxécuté par {ctx.author}")

        if username == "":
            if type(utils.get_binded(ctx.author.id)) == tuple:
                username, user_id, mode, color = utils.get_binded(ctx.author.id)
            else:
                await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
                return
        url = f"https://osuskills.com/user/{username}"
        embed = discord.Embed(title=f"skills de {username}", color=0xff66aa, timestamp=datetime.datetime.now(), url=url)

        leskill = BeautifulSoup(requests.get(url).content, "html.parser").find_all(class_="skillValue")
        # 1: Stamina, 2: Tenacity, 3: Agility, 4: Accuracy, 5: Precision, 6: Reaction, 7: Memory, 8: Reading
        categories = ["Stamina", "Tenacity", "Agility", "Accuracy", "Precision", "Reaction", "Memory", "Reading"]
        data = [int(s.text) for s in leskill]
        n = 0

        # ░ █
        # □ ■
        for i in data:
            progress = ["█" for j in range(0, 10) if j < i / 100]
            progress = progress + ["░" for k in range(10 - len(progress))]
            embed.add_field(name=f"{categories[n] + ': (' + str(i) + ')'}", value=f"{''.join(progress)}", inline=True)
            n += 1
        await ctx.send(embed=embed)

    
    @commands.command(name="statistics",
             aliases=["stats"],
             usage=f"{prefix}statistics <user> <mode>",
             brief="permet d'afficher les stats d'un joueur."
             )
    async def statistics(self, ctx, username: str = "", mode: str = "osu"):
        print(f"commande 'statistics' éxécuté par {ctx.author}")
        color = 0xff66aa

        if username == "":
            if type(utils.get_binded(ctx.author.id)) == tuple:
                username, user_id, mode, color = utils.get_binded(ctx.author.id)
            else:
                print(utils.get_binded(ctx.author.id))
                return await ctx.send("Tu peux mettre un pseudo ?"
                                    "\nou utilises `!o bind <url profil osu>`")

        data_z = OsuAPIv2.get_data_user(username, mode)
        if data_z.get('statistics') is not None:
            stats = data_z.get('statistics')
            grades = stats.get('grade_counts')
        else:
            return ctx.send(f'Impossible de charger les statistiques de {username}')
        heart = data_z.get('support_level') * emotes.get("Supporter")
        if data_z.get('support_level') == 0 and data_z.get('has_supported'):
            heart = emotes.get("WasSupporter")
        if data_z.get('is_online'):
            status = emotes.get("On")
        else:
            status = emotes.get("Off")

        embed = discord.Embed(color=color, title=f"{status} {data_z.get('username')}",
                            url=f"https://osu.ppy.sh/users/{data_z.get('id')}",
                            description=f"** ⸰ Supporter status:** {heart}"
                                        f"\n** ⸰ Twitter:** {data_z.get('twitter')}"
                                        f"\n** ⸰ mode:** {data_z.get('playmode')}"
                                        f"\n** ⸰ Discord:** {data_z.get('discord')}")

        embed.set_thumbnail(url=data_z['avatar_url'])
        embed.set_image(url=data_z['cover_url'])

        i = stats.get('level').get('progress') / 10
        progress = ["■" for j in range(0, 10) if j < i]
        progress = progress + ["□" for k in range(10 - len(progress))]

        # ░ ▒ ▒ ▓ █

        embed.add_field(name=f"__Statistiques de {data_z['username']} :flag_{data_z.get('country_code').lower()}: :__",
                        value=f"**Niveau:** `{stats.get('level').get('current')}` [{''.join(progress)}]"
                            f"\n**Accuracy:** `{round(stats.get('hit_accuracy'), 2)}%`"
                            f"\n**PP:** `{round(stats.get('pp'), 1)}pp`"
                            f"\n**Nombre de parties:** `{stats.get('play_count'):,}`"
                            f"\n**temps de jeu:** `{datetime.timedelta(seconds=stats.get('play_time'))}`"
                            f"\n**Classement Pays:** `{stats.get('country_rank'):,}`"
                            f"\n**Classement Global:** `{stats.get('global_rank'):,}`"
                            f"\n**Grades:** {emotes.get('A')}`{grades.get('a')}` {emotes.get('S')}`{grades.get('s')}`"
                            f" {emotes.get('SH')}`{grades.get('sh')}` {emotes.get('X')}`{grades.get('ss')}`"
                            f" {emotes.get('XH')}`{grades.get('ssh')}`",
                        inline=False)

        await ctx.send(embed=embed)


    @commands.command(name="fight",
                aliases=[],
                usage=f"{prefix}fight <user1> <user2> <type>",
                brief="permet de comparer sur plusieurs critères deux joueurs."
                )
    async def fight(self, ctx, USER: str = "planchapain ", USER2: str = "fayberiito", TYPE: str = ""):
        print(f"commande 'fight' éxécuté par {ctx.author}")

        if TYPE == "":
            embed_error = discord.Embed(title="Erreur de syntaxe", color=0xff69b4, )
            embed_error.add_field(name="Tu dois choisir une catégorie pour pouvoir lancer un combat, les "
                                    "catégories disponibles sont :", value="\n - playcount "
                                                                            "\n - rank "
                                                                            "\n - pp "
                                                                            "\n - accuracy "
                                                                            "\n - country_rank "
                                                                            "\n - total_score", inline=False)
            embed_error.set_footer(
                text="|made by Tarkor|", icon_url="http://s.ppy.sh/a/16748782")
            await ctx.send(embed=embed_error)
            return
        if USER == USER2:
            embed_error = discord.Embed(title="Les noms d'utilisateurs sont les mêmes", color=0xff69b4, )
            embed_error.add_field(name="Tu dois choisir des noms d'utilisateurs différents:",
                                value="\n par exemple : "
                                        "\n `!o fight Tarkor planchapain pp`", inline=False)
            embed_error.set_footer(
                text="|made by Tarkor|", icon_url="http://s.ppy.sh/a/16748782")
            await ctx.send(embed=embed_error)
            return
        data = OsuAPI.get_data_user(USER)
        data2 = OsuAPI.get_data_user(USER2)

        if data != [] and data2 != []:
            # store data USER

            playcount = data[0]["playcount"]
            total_score = data[0]["total_score"]
            pp_rank = data[0]["pp_rank"]
            pp_raw = data[0]["pp_raw"]
            accuracy = data[0]["accuracy"]
            pp_country_rank = data[0]["pp_country_rank"]

            # store data USER2

            playcount2 = data2[0]["playcount"]
            total_score2 = data2[0]["total_score"]
            pp_rank2 = data2[0]["pp_rank"]
            pp_raw2 = data2[0]["pp_raw"]
            accuracy2 = data2[0]["accuracy"]
            pp_country_rank2 = data2[0]["pp_country_rank"]

            embed = discord.Embed(title="combat entre les joueurs " + USER + " et " + USER2,
                                color=0xff66aa, )
            embed.set_footer(text="|made by Tarkor|", icon_url="http://s.ppy.sh/a/16748782")

            if TYPE == "playcount":
                if int(playcount) < int(playcount2):
                    winner = USER2
                    diff = round(float(playcount2)) - round(float(playcount))
                else:
                    winner = USER
                    diff = round(float(playcount)) - round(float(playcount2))

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{int(playcount):,}` parties."
                                    f"\n**__{USER2}:__** `{int(playcount2):,}` parties.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{int(diff):,}** parties jouées de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            elif TYPE == "rank":
                if int(pp_rank) < int(pp_rank2):
                    winner = USER
                    diff = round(float(pp_rank2)) - round(float(pp_rank))
                else:
                    winner = USER2
                    diff = round(float(pp_rank)) - round(float(pp_rank2))

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{int(pp_rank):,}`."
                                    f"\n**__{USER2}:__** `{int(pp_rank2):,}`.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{int(diff):,}** ranks de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            elif TYPE == "pp":
                if float(pp_raw) < float(pp_raw2):
                    winner = USER2
                    diff = round(float(pp_raw2)) - round(float(pp_raw))
                else:
                    winner = USER
                    diff = round(float(pp_raw)) - round(float(pp_raw2))

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{float(pp_raw):,}`pp."
                                    f"\n**__{USER2}:__** `{float(pp_raw2):,}`pp.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{int(diff):,}**pp de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            elif TYPE == "accuracy":
                if float(accuracy) < float(accuracy2):
                    winner = USER2
                    diff = round(float(accuracy2), 2) - round(float(accuracy), 2)
                else:
                    winner = USER
                    diff = round(float(accuracy), 2) - round(float(accuracy2), 2)

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{round(float(accuracy), 2)}`%."
                                    f"\n**__{USER2}:__** `{round(float(accuracy2), 2)}`%.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{round(diff, 2)}**% de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            elif TYPE == "country_rank":
                if int(pp_country_rank) < int(pp_country_rank2):
                    winner = USER
                    diff = round(float(pp_country_rank2)) - round(float(pp_country_rank))
                else:
                    winner = USER2
                    diff = round(float(pp_country_rank)) - round(float(pp_country_rank2))

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{int(pp_country_rank):,}`."
                                    f"\n**__{USER2}:__** `{int(pp_country_rank2):,}`.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{diff}** rank de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            elif TYPE == "total_score":
                if total_score < total_score2:
                    winner = USER2
                    diff = round(float(total_score2)) - round(float(total_score))
                else:
                    winner = USER
                    diff = round(float(total_score)) - round(float(total_score2))

                embed.add_field(name=f"\u200b",
                                value=f"**__{USER}:__** `{int(total_score):,}`."
                                    f"\n**__{USER2}:__** `{int(total_score2):,}`.",
                                inline=False)

                embed.add_field(name="\u200b",
                                value=f"**{winner}** a gagné."
                                    f"\nIl a **{diff:,}** score de plus !",
                                inline=False)
                await ctx.send(embed=embed)

            else:
                embed_error = discord.Embed(title="Erreur de syntaxe", color=0xff69b4, )
                embed_error.add_field(name="Tu dois choisir une catégorie existante:",
                                    value="\n par exemple " + TYPE + " n'hexiste pas, catégories possibles: "
                                                                    "\n - playcount "
                                                                    "\n - rank "
                                                                    "\n - pp "
                                                                    "\n - accuracy "
                                                                    "\n - country_rank "
                                                                    "\n - total_score", inline=False)
                embed_error.set_footer(
                    text="|made by Tarkor|", icon_url="http://s.ppy.sh/a/16748782")
                await ctx.send(embed=embed_error)

        else:
            embed_error = discord.Embed(title="Un des utilisateurs n'existe pas", color=0xff69b4, )
            embed_error.add_field(name="Tu dois choisir des noms d'utilisateurs existants:",
                                value="\n par exemple : "
                                        "\n `!o fight Tarkor planchapain pp`", inline=False)
            embed_error.set_footer(
                text="|made by Tarkor|", icon_url="http://s.ppy.sh/a/16748782")
            await ctx.send(embed=embed_error)


def setup(client):
    client.add_cog(Osu(client))