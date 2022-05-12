from urllib.parse import urlparse
import discord
import json
import requests
from discord.ext import commands

prefix = "!o "


class Fun(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(name="nsfw",
             aliases=[],
             usage=f"{prefix}nsfw",
             brief="commande réclammé par @Kiss-Shot#3173 et @Sacha#4422, affiche du nsfw."
             )
    async def nsfw(self, ctx):
        print(f"commande 'nsfw' éxécuté par {ctx.author}")
        r = requests.get("https://api.waifu.pics/nsfw/waifu").content.decode('utf8').replace("'", '"')
        s = json.dumps(json.loads(r), indent=4, sort_keys=True)
        await ctx.send(json.loads(s)["url"])


    @commands.command(name="waifu",
                aliases=[],
                usage=f"{prefix}waifu",
                brief="comme la commande nsfw, mais plus sfw."
                )
    async def waifu(self, ctx):
        print(f"commande 'waifu' éxécuté par {ctx.author}")
        r = requests.get("https://api.waifu.pics/sfw/waifu").content.decode('utf8').replace("'", '"')
        s = json.dumps(json.loads(r), indent=4, sort_keys=True)
        await ctx.send(json.loads(s)["url"])
    

def setup(client):
    client.add_cog(Fun(client))