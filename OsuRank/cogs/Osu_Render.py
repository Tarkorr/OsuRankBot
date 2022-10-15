from typing_extensions import ParamSpecKwargs
import discord
from discord.ext import commands
import asyncio
import datetime
from urllib.parse import urlparse
import Paginator
import json
import requests
import os
from pprint import pprint

prefix = "!o "
data_p = json.loads(open('players.json', "r").read())

class Osu_Render(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name="render",
             aliases=["r"],
             usage=f"{prefix}render",
             brief="permet de généré un rendu d'un gampley osu std. Grâce à un fichier de replay"
             )
    async def render(self, ctx):
        print(f"commande 'render' éxécuté par {ctx.author}")
        URL = "https://apis.issou.best/ordr/"

        if len(ctx.message.attachments) != 0:
            replay_url = ctx.message.attachments[0].url
            o = urlparse(replay_url)
            file = os.path.split(o.path)[1]

            if not file.endswith(".osr"):
                return await ctx.send(f"le fichier {file} n'est pas un fichier pris en compte,"
                                    f"\nseulement les fichiers se terminant par .osr sont acceptés.")

            file_request = requests.get(replay_url).content
            files = {
                'replayFile': ('OsuReplay.osr', file_request),
            }

            user_skin = "1"
            username = ctx.author.display_name
            params = None
            for p in data_p:
                if data_p[p]["discord_id"] == ctx.author.id:
                    username = str(data_p[p]["username"])
                    if data_p[p].get("skin") is not None:
                        user_skin = str(data_p[p].get("skin"))
                    if data_p[p].get('params'):
                        params = data_p[p]['params']

            values = {
                "username": username,
                "resolution": "1280x720",
                "skin": user_skin
            }
            if params != None:
                values = {**values, **params}
            print(values)
            current_time = datetime.datetime.now()
            cooldown = datetime.datetime.fromtimestamp(data_p['Jarod']['cooldown'])

            if cooldown - current_time >= datetime.timedelta(0):
                return await ctx.send(f"Merci de patienter 5 minutes entre chaque rendu."
                                    f"\nTemps restant estimé: *{cooldown - current_time}*")

            x = requests.post(url=URL + "renders", data=values, files=files)
            if x.status_code == 429:
                return await ctx.send("Trop de requètes..."
                                    f"\nMerci de patienter quelques secondes avant de réessayer. (dernière requète *{cooldown - current_time - datetime.timedelta(minutes=5, seconds=30)}*)")
            cooldown = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=30)
            data_p['Jarod']['cooldown'] = round(datetime.datetime.timestamp(cooldown))
            json.dump(data_p, open("players.json", "w"))

            # response format : {'errorCode': 0, 'message': 'Render added successfully', 'renderID': 331693}
            if x.status_code == 201:
                pot = x.json()
            else:
                await ctx.send(x.text)
                await ctx.send(x.content)
                await ctx.send(x)
                return await ctx.send("__Erreur.__" \
                                      f"\n*<@905448403092275230> requète de render:*" \
                                      f"\n__status:__ [<:status_dnd:887380229943865374> {x.status_code}]." \
                                      f"\n__time:__ {x.elapsed.total_seconds()}s" \
                                      f"\n__Reason:__ {x.reason}"
                                      f"\n__params:__ {values}")

            val = {
                "renderID": pot.get('renderID')
            }

            pat = requests.get(url=URL + "renders", params=val).json()['renders'][0]

            # t = datetime.datetime.strptime(pat['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # t = round(datetime.datetime.timestamp(t))

            embed = discord.Embed(title=pat['title'], color=0xff66aa, url=pat['replayFilePath'])
            embed.add_field(name="Rendering status :", value="[Request Sent]")
            embed.add_field(name="Render :", value=f"resolution: `{pat.get('resolution')}`"
                                                f"\nMods: `{pat.get('replayMods')}`"
                                                f"\nMap: [Download]({pat.get('mapLink')})"
                                                f"\nskin: {pat.get('skin')}")
            load = await ctx.send(embed=embed)

            while pat.get('progress') != "Done.":
                pat = requests.get(url=URL + "renders", params=val).json()['renders'][0]
                embed.set_field_at(0, value=pat.get('progress'), name="Rendering status :")
                await asyncio.sleep(7.5)
                await load.edit(embed=embed)

            return await ctx.send(pat['videoUrl'])
        else:
            return await ctx.send("Fichier manquant.")


    @commands.command(name="skin",
                aliases=[],
                usage=f"{prefix}skin [show, set, search] <id>",
                brief=f"Affiche tous les skins disponibles pour `{prefix}render` 'set' pour définir le skin"
                )
    async def skin(self, ctx, param: str = "", skin_id = ""):
        print(f"commande 'skin' éxécuté par {ctx.author}")
        URL = "https://apis.issou.best/ordr/"
        params = {
            "pageSize": 1000,
            "page": 1
        }
        skins = requests.get(url=URL + "skins", params=params).json()['skins']
        # pprint(requests.get(url=URL + "skins").json())
        # !o reload Osu_Render
        embeds = []
        if param == "search":
            p = {
            "pageSize": 1000,
            "page": 1,
            "search": skin_id
            }
            sk = requests.get(url=URL + "skins", params=p).json()['skins']
            limit = 0
            a = ""
            
            if len(sk) < 10:
                for el in sk:
                    a = a + f"\n**{el['presentationName']}** (`{el['id']}`) \nby *{el['author']}*"      
            
                emb = discord.Embed().add_field(name='__Available Skins :__', value=a)
                return await ctx.send(embed=emb)
            
            for el in sk:
                if limit < 8:
                    a = a + f"\n**{el['presentationName']}** (`{el['id']}`) \nby *{el['author']}*"
                    limit += 1
                else:
                    a = a + f"\n**{el['presentationName']}** (`{el['id']}`) \nby *{el['author']}*"
                    p = discord.Embed().add_field(name='__Available Skins :__', value=a)
                    embeds.append(p)
                    limit = 0
                    a = ""

            await Paginator.Simple().start(ctx, pages=embeds)

        if param == "set":
            if skin_id == None:
                return await ctx.send("il manque l'`id` du skin."
                                    "\n__exemple:__ `!o set 23` avec pour `id` 23.")
            try:
                skin_id = int(skin_id)
            except ValueError as V:
                return await ctx.send("l'`id` du skin, n'est pas un id de skin."
                                      "\n__exemple:__ `!o set 23` avec pour `id` 23.")
            for p in data_p:
                if data_p[p]["discord_id"] == ctx.author.id:
                    for el in skins:
                        if skin_id == el['id']:
                            data_p[p]["skin"] = skin_id
                            json.dump(data_p, open("players.json", "w"))
                            embed = discord.Embed().add_field(name=f":white_check_mark: **__{el['presentationName']}__**",
                                                            value=f"by *{el['author']}* - [[Download]({el['url']})]"
                                                                    f"\nCe skin a été définis en tant que skin par défaut"
                                                                    f" pour chaque rendu."
                                                                    f"\n*(les images prennent un peu de temps à charger)*")
                            embed.set_image(url=el['highResPreview'])
                            return await ctx.send(embed=embed)

                    return await ctx.send(f"`{skin_id}` n'est pas valide."
                                        f"\nla liste de skin et de leurs ids est visible en faisant `{prefix}skin`")
            return await ctx.send("Pour pouvoir définir un skin et des paramètres particuliers,"
                                f"\nil faut être bind avec le bot, exécute la commande "
                                f"`{prefix}bind (url de ton profil osu)`")

        if param == "show":
            try:
                skin_id = int(skin_id)
            except ValueError:
                return await ctx.send(f"`{skin_id}` n'est pas un id de skin.")
            
            for el in skins:
                if skin_id == el['id']:
                    user_skin = str([data_p[p].get('skin') for p in data_p if data_p[p]["discord_id"] == ctx.author.id])
                    em = "#"
                    if str(f"[{skin_id}]") == user_skin:
                        em = ":white_check_mark:"
                    embed = discord.Embed().add_field(name=f"{em} **__{el['presentationName']}__**",
                                                    value=f"by *{el['author']}* - [[Download]({el['url']})]"
                                                            f"\n*(les images prennent un peu de temps à charger)*")
                    embed.set_image(url=el['gridPreview']).set_thumbnail(url=el['highResPreview'])
                    return await ctx.send(embed=embed)
            return await ctx.send(f"`{skin_id}` n'est pas un id valide.")
        else:
            limit = 0
            a = ""
            for el in skins:
                if limit < 8:
                    a = a + f"\n**{el['presentationName']}** (`{el['id']}`) \nby *{el['author']}*"
                    limit += 1
                else:
                    a = a + f"\n**{el['presentationName']}** (`{el['id']}`) \nby *{el['author']}*"
                    p = discord.Embed().add_field(name='__Available Skins :__', value=a)
                    embeds.append(p)
                    limit = 0
                    a = ""

            await Paginator.Simple().start(ctx, pages=embeds)
        
    @commands.command(name="params",
            aliases=[],
            usage=f"{prefix}params [set, reset] <param> <value>",
            brief=f"Affiche tous les paramètres disponibles pour `{prefix}render` 'set' pour définir le paramètre,"
            f"\navec `{prefix}params reset all` pour reset tous les paramètres."
            )
    async def params(self, ctx, c: str = "", param: str = "", value = ""):
        base_parameters = {
            "globalVolume": 50,
            "musicVolume": 50,
            "hitsoundVolume": 50,
            "showHitErrorMeter": "true",
            "showUnstableRate": "true",
            "showScore": "true",
            "showHPBar": "true",
            "showComboCounter": "true",
            "showPPCounter": "true",
            "showScoreboard": "false",
            "showBorders": "false",
            "showMods": "true",
            "showResultScreen": "true",
            "useSkinCursor": "true",
            "useSkinColors": "false",
            "useSkinHitsounds": "true",
            "useBeatmapColors": "true",
            "cursorScaleToCS": "false",
            "cursorRainbow": "false",
            "cursorTrailGlow": "false",
            "drawFollowPoints": "true",
            "scaleToTheBeat": "false",
            "sliderMerge": "false",
            "objectsRainbow": "false",
            "objectsFlashToTheBeat": "false",
            "useHitCircleColor": "true",
            "seizureWarning": "false",
            "loadStoryboard": "true",
            "loadVideo": "true",
            "introBGDim": 0,
            "inGameBGDim": 75,
            "breakBGDim": 30,
            "BGParallax": "false",
            "showDanserLogo": "true",
            "skip": "true",
            "cursorRipples": "false",
            "cursorSize": 1,
            "cursorTrail": "true",
            "drawComboNumbers": "true",
            "sliderSnakingIn": "true",
            "sliderSnakingOut": "true",
            "showHitCounter": "false",
            "showKeyOverlay": "true",
            "showAvatarsOnScoreboard": "false",
            "showAimErrorMeter": "false",
            "playNightcoreSamples": "true"
        }
        ints = ["globalVolume", "musicVolume", "hitsoundVolume", "introBGDim", "inGameBGDim", "breakBGDim"]

        if c == "set":
            if param == None or value == None:
                return await ctx.send("il manque la moitié de la commande."
                                      "\n__exemple:__ `!o params set globalVolume 51`.")
            elif param in ints:
                try:
                    value = int(value)
                except ValueError:
                    return await ctx.send(":flushed: Attention ce que tu as envoyé n'est pas un chiffre. Ici la valeur demandé est un chiffre.")
            elif param == "cursorSize":
                try:
                    value = float(value)
                except ValueError:
                    return await ctx.send(":flushed: Attention ce que tu as envoyé n'est pas un chiffre. Ici la valeur demandé est un chiffre. (à virgule celui là, si ça marche pas envois 1.0 par acquis de conscience.)")
            else:
                if value.lower() == "false" or value.lower() == "true":
                    value = value.lower()
                else:
                    return await ctx.send(":flushed: Attention ce que tu as envoyé n'est pas un booléen. Ici la valeur demandé est un booléen donc `true` ou `false`. (ou bool quand t'es un mec cool)")
            
            for p in data_p:
                if data_p[p]["discord_id"] == ctx.author.id:
                    if not data_p[p].get('params'):
                        data_p[p]['params'] = base_parameters
                        json.dump(data_p, open("players.json", "w"))
                    for parameter in data_p[p]['params']:
                        if param == parameter:
                            print(f"param found it is ({parameter})")
                            data_p[p]['params'][param] = value
                            
                            json.dump(data_p, open("players.json", "w"))
                            embed = discord.Embed(color = int(data_p[p]['color'], 16) ).add_field(name='__Paramètre changé:__', value=f"```{param}: {data_p[p]['params'][param]}```")
                            return await ctx.send(embed=embed)

                    return await ctx.send(f"`{param}` n'est pas valide."
                                        f"\nla liste de skin et de leurs ids est visible en faisant `{prefix}skin`")
            return await ctx.send("Pour pouvoir définir un skin et des paramètres particuliers,"
                                f"\nil faut être bind avec le bot, exécute la commande"
                                f"`{prefix}bind (url de ton profil osu)`")

        if c == "reset":
            if param == "all":
                for p in data_p:
                    if data_p[p]["discord_id"] == ctx.author.id:
                        data_p[p]['params'] = base_parameters
                        json.dump(data_p, open("players.json", "w"))
                        
                        text = "```" + ''.join([f"{pppp}: {data_p[p]['params'][pppp]}\n" for pppp in data_p[p]['params']]) + "```"
                        embed = discord.Embed(color = int(data_p[p]['color'], 16) ).add_field(name='__Paramètres actuels:__', value=text)
                        return await ctx.send(embed=embed)
                return await ctx.send("Pour pouvoir définir un skin et des paramètres particuliers,"
                                f"\nil faut être bind avec le bot, exécute la commande"
                                f"`{prefix}bind (url de ton profil osu)`")
        else:
            for p in data_p:
                if data_p[p]["discord_id"] == ctx.author.id:
                    if not data_p[p].get('params'):
                        data_p[p]['params'] = base_parameters
                        json.dump(data_p, open("players.json", "w"))
                    
                    
                    limit = 0
                    a = "```"
                    embeds = []
                    UrParams = data_p[p]['params']
                    for pppp in UrParams:
                        if limit < 14:
                            a = a + f"{pppp}: {'✅' if UrParams[pppp] == 'true' else ''}{'❌' if UrParams[pppp] == 'false' else ''}{f'{UrParams[pppp]}%' if type(UrParams[pppp]) == int and pppp != 'cursorSize' else ''}{f'{UrParams[pppp]}' if pppp == 'cursorSize' else ''}\n"
                            limit += 1
                        else:
                            a = a + f"{pppp}: {'✅' if UrParams[pppp] == 'true' else ''}{'❌' if UrParams[pppp] == 'false' else ''}{f'{UrParams[pppp]}%' if type(UrParams[pppp]) == int and pppp != 'cursorSize' else ''}{f'{UrParams[pppp]}' if pppp == 'cursorSize' else ''}```"
                            p = discord.Embed().add_field(name='__Available parameters:__', value=a)
                            embeds.append(p)
                            limit = 0
                            a = "```"

                    await Paginator.Simple().start(ctx, pages=embeds)
                
            return await ctx.send("Pour pouvoir définir un skin et des paramètres particuliers,"
                            f"\nil faut être bind avec le bot, exécute la commande"
                            f"`{prefix}bind (url de ton profil osu)`")


async def setup(client):
    await client.add_cog(Osu_Render(client))