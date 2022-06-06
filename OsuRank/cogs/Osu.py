import datetime
import os
import typing
from typing_extensions import ParamSpecKwargs
import discord
import json
import requests
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from OsuRank.utils import OsuAPIv2, OsuAPI, utils, OsuAPIv3
from OsuRank.utils import display_score as dp
from bs4 import BeautifulSoup
from pprint import pprint
import time

prefix = "!o "
data_p = json.loads(open('players.json', "r").read())

class KEYS:
    cfg = json.loads(open("config_OSU.json", "r").read())
    my_id = int(cfg["me"])
    token = cfg["token"]
    guild_id = cfg["server-id"]
    logs_channel = cfg["logs-channel-id"]


class Osu(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.binding_message = f"Pour pouvoir utiliser cette commande tu (ou la personne que tu as ping) as besoin d'être lié avec le bot. Pour être lié il te suffit de faire la commande `{prefix}bind \"url de ton profil osu\"`," \
                               f"\nMerci de ne pas mettre un autre profil que le tiens. Être lié avec le bot te permetteras de pouvoir exécuter la plupart des commandes et aussi de choisir un skin pour la commande `{prefix}render` Ainsi que de pouvoir utiliser la commande `{prefix}last_play_compare`"
        self.API = OsuAPIv3.API()
    

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
                
                play = self.API.get_user_beatmap_score(beatmap_id=beatmap_id, user=user_id).get('score')
                                
                await message.edit(embed=utils.generate_embed_score(play, "Best "))
                await message.remove_reaction(emoji, user)

        elif emoji == '⏰':
            embed = message.embeds[0]

            if "completed by" in embed.author.name:

                user_id = os.path.split(embed.author.url)[1]
                beatmap_id = os.path.split(embed.url)[1]

                score = self.API.get_user_beatmap_score(beatmap_id=beatmap_id, user=user_id).get('score')
                
                if score != None:
                    mode = str(score.get('mode'))
                else:
                    return await message.edit("UwUn't, ptit prob réessaies.")
                recent_maps = self.API.get_user_score(user=user_id, mode=mode, score_type='recent')
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

    
    @commands.command(aliases=['t'],
             name="tournament",
             usage=f"{prefix}tournament <user1> <user2> <bo>",
             brief="permet de faire un petit 'best of' (bo) entre 2 personnes."
             )
    async def tournament(self, ctx, user1: str = "", user2: str = "", bo: int = 3):
        print(f"commande 'tournament' éxécuté par {ctx.author}")
        # :white_large_square:  :blue_square:  :red_square:

        embed_score = discord.Embed(title=f"__{user1} vs {user2}:__", color=0xff69b4)

        base = ":white_large_square:"
        bo = int((bo + 1) / 2)
        embed_score.add_field(name=f"__{user1}:__", value=f"{base * bo}", inline=True)
        embed_score.add_field(name=f"__{user2}:__", value=f"{base * bo}", inline=True)
        embed_score.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        score = await ctx.send(embed=embed_score)
        emojis = ['🟦', '🟥', '🔄']
        for emoji in emojis:
            await score.add_reaction(emoji)
    
    
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
        data = self.API.search(query=query, mode=mode)
        users = []
        data = data.get('user')
        if data !=None:
            data = data.get('data')
        else:
            await ctx.send("erreur..")
        if data != None:
            print(data)
            for i in range(len(data)):
                users.append(data[i].get("username"))
            gamers = ' \n'.join(users)
            await ctx.send(f" first {len(data)} founds, users names : \n{gamers}")
        else:
            await ctx.send("erreur...")
    

    @commands.command(name="last_play",
             aliases=["lp"],
             usage=f"{prefix}last_play <user> <mode>",
             brief="affiche le dernier score de <user>."
             )
    async def last_play(self, ctx,
                        username: str = "",
                        mode: str = "osu"):

        bme = ["<", "@", ">"]
        discord_id = None
        osu_id = None
        
        # Ping d'une personne.
        if any(x in username for x in bme):
            discord_id = username
            for b in bme:
                if b in discord_id:
                    discord_id = discord_id.replace(b, "")
            
            try:
                discord_id = int(discord_id)
            except ValueError as e:
                return await ctx.send(f"{username} est un Rôle ou autre, merci de ping une personne.")
        
        # user peut être quelqu'un ?
        elif username != "":
            if mode not in utils.osu_modes:
                return await ctx.send(f"bah {mode} n'est pas un mode.")
            else:
                data_m = self.API.get_user(user=username, mode=mode)

            if data_m == {}:
                return await ctx.send(f"erreur {username} n'éxiste pas.")
            
            osu_id = str(data_m.get('id'))
            mode = str(data_m.get('mode'))
            username = str(data_m.get('username'))
        
        # Sinon
        if discord_id is not None:
            user_infos = utils.get_binded(int(discord_id))
        elif osu_id is not None:
            user_infos = utils.get_binded(ctx.author.id)
        else:
            user_infos = utils.get_binded(ctx.author.id)
        
        if user_infos != None:
            if osu_id is None:
                osu_id = user_infos.get("osu_id")
                mode = user_infos.get("mode")
            if username == "":
                username = user_infos.get("username")
            discord_id = user_infos.get("discord_id")
            color = int(user_infos.get("color"), 16)
        else:
            return await ctx.send(self.binding_message)

        play = self.API.get_user_score(user = osu_id, score_type = "recent", mode = mode, limit = 1)

        if play == {} or play == []:
            return await ctx.send(f"{username} n'a pas de parties récentes.")
        else:
            play = play[0]

        rank_embed = await ctx.send(embed=utils.generate_embed_score(play, "Last ", color))
        for emoji in ['🏆', '⏰']:
            await rank_embed.add_reaction(emoji)


    @commands.command(name="last_play_compare",
             aliases=["lpc"],
             usage=f"{prefix}last_play_compare <param>",
             brief="affiche le dernier score de la personne qui éxecute la commande et les compare avec..."
             )
    async def last_play_compare(self, ctx, param: str = ""):
        print(f"commande 'last_play_compare' éxécuté par {ctx.author}")
        
        for p in data_p:
            if str(ctx.author.id) == str(data_p[p]["discord_id"]):
                user_id = str(data_p[p]["osu_id"])
                mode = str(data_p[p]["mode"])
                username = str(data_p[p]["username"])
                rival = data_p[p].get("rival")
                player = p
                break
        else:
            return await ctx.send(self.binding_message)
            
        def CheckMess(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel
        
        if param == "setup":
            # en gros soit chaque rep après ce mess ou kwargs
            await ctx.send("OK ! Merci de m'envoyer le nom de 5 joueurs, qui bien entendu ne te surpasseront jamais "
                           "mais bien entendu il faut savoir leurs démontrer que des fois tu fais preuve de faiblesse..."
                           "\nBref, Pour que je puisse enregistrer les mecs nuls qui éssaient de te dépasser "
                           "envois moi un message du style: \nFayberiito, Planchapain, regress Joksath, silverxs83, chocomint")
            
            try:
                msg = await self.client.wait_for("message", timeout = 60, check = CheckMess)
            except:
                return await ctx.reply("HEY ! T'as oublié de me l'envoyer ce message ???")
            
            # print(msg)
            print(msg.content)
            rep = msg.content
            rivals = rep.split(", ")
            if len(rivals) > 5:
                return await ctx.send("Pas Plus de 5 joueurs, réessaies.")
            
            data_sup = [self.API.get_user(user=r, mode=mode) for r in rivals]
            ricard = []
            for d in data_sup:
                if d == {} or d is None:
                    return await ctx.send(f"ptit problème là c'est qui {rivals[data_sup.index(d)]}")
                # dict(d)
                ricard.append([d.get("id"), d.get("username")])
                stats = d.get("statistics")
                country_code = d.get('country_code')
                if stats != None and country_code != None:
                    await ctx.send(f":flag_{country_code.lower()}: **{d.get('username')}** avec `{int(stats.get('pp')):,}`pp.")
            
            # pprint(data_sup[2], compact=True)
            data_p[player]["rival"] = ricard
            json.dump(data_p, open("players.json", "w"))
            await ctx.send("Nickel mon pote, t'as tout compris enfin j'espère que les mecs que tu veux fumer c'est bien eux.")
            return

        else:
            if rival is None:
                return await ctx.send("il semblerait que tu n'es pas définis de personne avec qui comparer"
                                    "\nPour le faire fais `!o lpc setup`")
            else:
                print(f"good {rival}")
                    
            play = OsuAPIv2.get_data_user_recent(user_id=user_id, mode=mode)
                
            if not play:
                return await ctx.send(f"{username} n'a pas de parties récentes.")
            else:
                play = play[0]
                
            # pprint(play, compact=True)
            beatmap = play.get('beatmap')
            beatmapset = play.get('beatmapset')
            
            # copie de la liste de rival
            rival_ = list(rival)
            # rajoute l'auteur de la commande
            rival_.append([user_id, username])
            n = 0
            
            for r in rival_:
                if r[0] == int(user_id):
                    rival_.append(play.get('score'))
                else:
                    dang = OsuAPIv2.get_data_user_score(map_id=beatmap.get("id"), user_id=r[0], mode=mode)
                    if dang is not None:
                        rival_[n].append(dang.get('score').get('score'))
                    else:
                        rival_[n].append(0)
                n += 1
            
            rival_ = sorted(rival_, key=lambda x: x[2])
            rival_.reverse()
            print(rival_)
            
            comp = []
            
            fields = []
            for r in rival_:
                field = ""
                if r[0] == int(user_id):
                    bing = play
                else:
                    dang = OsuAPIv2.get_data_user_score(map_id=beatmap.get("id"), user_id=r[0], mode=mode)
                    bing = None
                    if dang is not None:
                        bing = dang.get("score")
                # 0: Rank, 1: FC, 2: pp, 3: score, 4: combo, 5: acc,
                # pprint(dang)
                
                if bing is not None:
                    # pprint(bing)

                    field = field + f"\n**__[{r[1]}](https://osu.ppy.sh/scores/mania/{bing.get('id')})__**:" \
                                    f"\n**rank:** {utils.emotes.get(bing.get('rank'))}|- - - - - - - - - - - - - - - - -| **pp:** `{round(bing.get('pp'))}`pp" \
                                    f"\n**accuracy:** `{round(float(bing.get('accuracy')*100), 2)}`*%* |- - - - - - - - - -| **combo:** `{bing.get('max_combo')}`x"
                                    # f"\n - "
                                    # f" <--> [{bing.get('score')}]"
                else:
                    field = field + f"\n**{r[1]}**: {utils.emotes.get('0')}"
                
                fields.append(field)
                
                    
            stats = play.get('statistics')
            user = play.get('user')

            username = user.get('username')
            title = beatmapset.get('title')

            print(f"{username} completed the map {title}")
            # wprint(f"{username} completed the map {title}")

            color = 0xff66aa
            for p in data_p:
                if data_p[p]['osu_id'] == user.get('id'):
                    color = int(data_p[p]['color'], 16)

            t = datetime.datetime.strptime(play.get('created_at'), "%Y-%m-%dT%H:%M:%S+00:00")

            embed = discord.Embed(title="**" + title + "**", url=beatmap.get('url'), color=color, timestamp=t)

            if play.get("mode") == "mania":
                img_mode = "https://i.imgur.com/NVkykfe.png"
            elif play.get("mode") == "osu":
                img_mode = "https://i.imgur.com/bnSSOS9.png"
            elif play.get("mode") == "fruits":
                img_mode = "https://i.imgur.com/MjOv5Kd.png"
            else:
                img_mode = "https://i.imgur.com/iSQFSTn.png"

            embed.set_thumbnail(url=img_mode)
            embed.set_image(url=beatmapset.get('covers').get('card'))
            embed.set_author(name=f"{beatmap.get('status')} completed by {username}", url="https://osu.ppy.sh/users/"+ str(user.get('id')),
                            icon_url=user.get('avatar_url'))
            # ☆☆☆
            length = str(time.strftime('%M:%S', time.gmtime(int(beatmap.get("total_length")))))
            stars = beatmap.get('difficulty_rating')
            embed.add_field(name=" __Beatmap informations:__ ", value=f"\n **__Durée:__** `{length}` "
                                                                    f"\n **__stars:__** `{stars}☆`", inline=False)

            if not play.get('mods'):
                mods = "No Mod"
            else:
                mods = ', '.join(play.get('mods'))

            if play.get("pp") is not None:
                pp = int(round(play.get('pp')))
            else:
                pp = 0

            emote_rank = utils.emotes.get(play.get("rank"))
            tot = ""
            i_ = 0
            for f in fields:
                tot = tot + f
                if len(tot) > 500 and i_ == 0:
                    embed.add_field(name=f"**__Score Comparaison:__**", value=tot,
                            inline=False)
                    tot = ""
                    i_ += 1
            if len(tot) > 0:
                embed.add_field(name=f"\u200b" , value=tot,
                                inline=False)
            
            await ctx.send(embed=embed)

    

    @commands.command(name="rank",
             aliases=[],
             usage=f"{prefix}rank <user> <mode>",
             brief="affiche sur une petite carte le rank de <user>."
             )
    async def rank(self, ctx, USER: str = "", MODE: str = "osu"):
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

        data_m = self.API.get_user(user=USER, mode=MODE)
        if data_m == {}:
            return await ctx.send(f"mmmh ? {USER} n'a jamais joué à osu!")

        baseImage = Image.open("OsuRank/cards/card_osu_V1.png")

        if ctx.author == self.client.get_user(KEYS.my_id):
            await ctx.send("Bonjour Maître.")
            baseImage = Image.open("OsuRank/cards/card_Tarkor.png")
        if ctx.author == self.client.get_user(566879332606410752):
            baseImage = Image.open("OsuRank/cards/cardSacha.png")
        if ctx.author == self.client.get_user(455285319831519234):
            baseImage = Image.open("OsuRank/cards/cardFayber.png")

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
        Username_font = "OsuRank/cards/Ubuntu.ttf"
        Username_font = ImageFont.truetype(Username_font, 50)
        image_editable.text(Username_pos, username, fill=color, font=Username_font)

        # level
        level_pos = (185, 108)
        level_font = "OsuRank/cards/Ubuntu.ttf"
        level_font = ImageFont.truetype(level_font, 43)
        image_editable.text(level_pos, str(round(float(level))), fill=color, font=level_font)

        # rank
        Rank_pos = (570, 35)
        Rank_font = "OsuRank/cards/Ubuntu.ttf"
        Rank_font = ImageFont.truetype(Rank_font, 40)
        image_editable.text(Rank_pos, pp_rank, fill=color, font=Rank_font)

        # pp
        pp_pos = (387, 112)
        pp_font = "OsuRank/cards/Ubuntu.ttf"
        pp_font = ImageFont.truetype(pp_font, 40)
        image_editable.text(pp_pos, str(round(float(pp_raw))), fill=color, font=pp_font)

        baseImage.save("OsuRank/cards/card.png")
        await ctx.send(file=discord.File("OsuRank/cards/card.png"))
    

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

            data_o = self.API.get_user(user=osu_id)

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
            player = utils.get_binded(ctx)
            if player is None:
                return await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
            else:
                user = player.get("username")
                mode = player.get("mode")
            

        data_m = OsuAPIv2.get_data_user(user_id=user, mode=mode)
        if data_m == "404":
            # relou, parce que quand on le fait pour soit même bah ça mets l'id
            return await ctx.send(f"mmmh ? {user} n'a jamais joué à osu!")
        elif data_m is None:
            return await ctx.send("Error: data is None")

        if mode == '':
            mode = data_m['playmode']
        else:
            # aucune verification de si MODE existe vraiment pas fou ngl.
            # j'ai écris le commentaire au dessus je sais pas quand du coup je comprends pas :/
            mode = mode
        user_id = str(data_m['id'])
        map_id = os.path.split(url)[1]

        play = OsuAPIv2.get_data_user_score(user_id=user_id, map_id=map_id, mode=mode)
        if play is None:
            return await ctx.send("eror")
        play = play.get('score')
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
            player = utils.get_binded(ctx.author.id)
            if player is None:
                return await ctx.send("Tu peux mettre un pseudo ?"
                                      "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
            else:
                user = player.get("username")
                mode = player.get("mode")
                user_id = str(player.get("osu_id"))
                color = int(player.get('color'), 16)
        else:
            color = 0xff69b4
            data_o = self.API.get_user(user=username, mode=mode)

            if data_o == {}:
                return await ctx.send(f"mmmh ? {username} n'a jamais joué à osu!")
            user_id = data_o['id']

        data_m = self.API.get_user_score(user=user_id, mode=mode, limit=limit, score_type="best")

        embed = discord.Embed(color=color, title=f"Meilleurs scores de {username}")
        for result in data_m:
            beatmap = result.get("beatmap")
            beatmapset = result.get("beatmapset")
            stats = result.get("statistics")
            emote_rank = utils.emotes.get(result.get("rank"))
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

                data_u = self.API.get_user(user=data_p[p]["osu_id"], mode=data_p[p]["mode"])

                stats = data_u.get('statistics')
                if stats is None:
                    return await ctx.send("problemo tengo el mismo pardono.")

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
            player = utils.get_binded(ctx)
            if player is None:
                return await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
            else:
                username = player.get("username")
                mode = player.get("mode")
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
            player = utils.get_binded(ctx)
            if player is None:
                return await ctx.send("Tu peux mettre un pseudo ?"
                            "\nFais `!o bind <url profil osu>` pour pouvoir directement utiliser `!o lp`")
            else:
                username = str(player.get("osu_id"))
                mode = player.get("mode")

        data_z = self.API.get_user(user=username, mode=mode)
        stats = data_z.get('statistics')
        if stats is not None:
            grades = stats.get('grade_counts')
        else:
            return await ctx.send(f'Impossible de charger les statistiques de {username}')
        
        heart = data_z.get('support_level')
        if heart is None:
            heart = ""
        else:
            heart = heart * utils.emotes.get("Supporter")
        if data_z.get('support_level') == 0 and data_z.get('has_supported'):
            heart = utils.emotes.get("WasSupporter")
        if data_z.get('is_online'):
            status = utils.emotes.get("On")
        else:
            status = utils.emotes.get("Off")

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
        
        country_code = data_z.get('country_code')
        if country_code is None:
            country_code = ""

        embed.add_field(name=f"__Statistiques de {data_z['username']} :flag_{country_code.lower()}: :__",
                        value=f"**Niveau:** `{stats.get('level').get('current')}` [{''.join(progress)}]"
                            f"\n**Accuracy:** `{round(stats.get('hit_accuracy'), 2)}%`"
                            f"\n**PP:** `{round(stats.get('pp'), 1)}pp`"
                            f"\n**Nombre de parties:** `{stats.get('play_count'):,}`"
                            f"\n**temps de jeu:** `{datetime.timedelta(seconds=stats.get('play_time'))}`"
                            f"\n**Classement Pays:** `{stats.get('country_rank'):,}`"
                            f"\n**Classement Global:** `{stats.get('global_rank'):,}`"
                            f"\n**Grades:** {utils.emotes.get('A')}`{grades.get('a')}` {utils.emotes.get('S')}`{grades.get('s')}`"
                            f" {utils.emotes.get('SH')}`{grades.get('sh')}` {utils.emotes.get('X')}`{grades.get('ss')}`"
                            f" {utils.emotes.get('XH')}`{grades.get('ssh')}`",
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
        data = self.API.get_user(user=USER)
        data2 = self.API.get_user(user=USER2)

        if data != {} and data2 != {}:
            
            statistics = data.get('statistics')
            statistics2 = data2.get('statistics')
            
            if statistics is None or statistics2 is None:
                return await ctx.send('erreur.')
            
            # store data USER

            playcount = statistics.get("play_count")
            total_score = statistics.get("total_score")
            pp_rank = statistics.get("global_rank")
            pp_raw = statistics.get("pp")
            accuracy = statistics.get("hit_accuracy")
            pp_country_rank = statistics.get("country_rank")

            # store data USER2

            playcount2 = statistics2.get("play_count")
            total_score2 = statistics2.get("total_score")
            pp_rank2 = statistics2.get("global_rank")
            pp_raw2 = statistics2.get("pp")
            accuracy2 = statistics2.get("hit_accuracy")
            pp_country_rank2 = statistics2.get("country_rank")

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