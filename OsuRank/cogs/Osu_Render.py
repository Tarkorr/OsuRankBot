import discord
from discord.ext import commands
import asyncio
import datetime
from urllib.parse import urlparse
from PycordPaginator import Paginator
import json
import requests
import os

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

            for p in data_p:
                if data_p[p]["discord_id"] == ctx.author.id:
                    username = str(data_p[p]["username"])
                    if data_p[p].get("skin") is not None:
                        user_skin = str(data_p[p].get("skin"))

            values = {
                "username": username,
                "resolution": "1280x720",
                "skin": user_skin
            }
            current_time = datetime.datetime.now()
            cooldown = datetime.datetime.fromtimestamp(data_p['Jarod']['cooldown'])

            if cooldown - current_time >= datetime.timedelta(0):
                return await ctx.send(f"Merci de patienter 5 minutes entre chaque rendu."
                                    f"\nTemps restant estimé: *{cooldown - current_time}*")

            x = requests.post(url=URL + "renders", data=values, files=files)
            if x.status_code == 429:
                return await ctx.send("Trop de requètes..."
                                    "\nMerci de patienter quelques secondes avant de réessayer.")
            cooldown = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=30)
            data_p['Jarod']['cooldown'] = round(datetime.datetime.timestamp(cooldown))
            json.dump(data_p, open("players.json", "w"))

            # response format : {'errorCode': 0, 'message': 'Render added successfully', 'renderID': 331693}
            if x.status_code == 201:
                pot = x.json()
            else:
                return await ctx.send("fail.")

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
                usage=f"{prefix}skin [show, set] <id>",
                brief=f"Affiche tous les skins disponibles pour `{prefix}render` 'set' pour définir le skin"
                )
    async def skin(self, ctx, param: str = "", skin_id: int = None):
        print(f"commande 'skin' éxécuté par {ctx.author}")
        URL = "https://apis.issou.best/ordr/"
        skins = requests.get(url=URL + "skins").json()['skins']
        embeds = []

        if param == "set":
            if skin_id is None:
                return await ctx.send("il manque l'`id` du skin."
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
                                        f"la liste de skin et de leurs ids est visible en faisant `{prefix}skin`")
            return await ctx.send("Pour pouvoir définir un skin et des paramètres particuliers,"
                                f"\nil faut être bind avec le bot, exécute la commande "
                                f"`{prefix}bind (url de ton profil osu)`")

        if param == "show":
            if type(skin_id) == int:
                for el in skins:
                    if skin_id == el['id']:
                        user_skin = str([data_p[p].get('skin') for p in data_p if data_p[p]["discord_id"] == ctx.author.id])
                        em = "#"
                        print(f"{user_skin}", skin_id)
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

            e = Paginator(client=self.client.components_manager, embeds=embeds, channel=ctx.channel,
                        only=ctx.author, ctx=ctx, use_select=False)
            return await e.start()


def setup(client):
    client.add_cog(Osu_Render(client))