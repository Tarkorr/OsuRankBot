import discord
from discord.ext import commands
from pycord_components import PycordComponents
from discord.ext.commands import CommandNotFound
import os
import json

cfg = json.loads(open("config_OSU.json", "r").read())
class KEYS:
    OSU_API = cfg["OSU_API"]
    my_id = int(cfg["me"])
    token = cfg["token"]
    guild_id = cfg["server-id"]
    logs_channel = cfg["logs-channel-id"]


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!o ",  guild_subscriptions=True, intents=intents)

print("Script executed OwO")

@client.event
async def on_ready():
    PycordComponents(client)
    game = discord.Game("Diplomacy")
    await client.change_presence(status=discord.Status.dnd, activity=game)
    print(client.user.name + f' <!> - connecté - <!> {round(client.latency, 2)}s')
    me = client.get_user(KEYS.my_id)
    await me.send('Bot online !')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@client.event
async def on_member_join(member):
    b = 0
    if member.id == 384405903471804427:
        await member.kick(reason="error")
        print(f"dégage {b}")
        b += 1


@client.event
async def on_message(ctx):
    content = ctx.content
    if ctx.author.id == 913937262016872518:
        return
    if "yuno gasai" in content.lower():
        print(f"{ctx.author} IS SAYING THE BANNED WORD")
        await ctx.reply(f"yuno gasai for real ? \nhop hop hop ta gueule.")
        roles = ctx.guild.roles
        role = discord.utils.get(roles, name="👑")
        role_c = discord.utils.get(roles, name="cringelord")

        if role_c in roles:
            await ctx.author.remove_roles(role_c)
        role_c = discord.utils.get(roles, name="cringelord")
        await ctx.author.add_roles(role_c)

    if "cringe" in content.lower():
        await ctx.reply(f"S'exprimer d'une manière si limité... "
                        f"\nva donc lire ceci "
                        f"https://mangadex.org/title/49c7b586-b0a3-4776-b3f5-3bdc62d82161/dog-nigga jeune chevalier."
                        f"\nEn espérant que tu sois éclairé par le génie de cet ouvrage, et que tu deviennes une "
                        f"personne drastiquement plus intelligente.")
    if "ez" in content.lower():
        await ctx.reply("mmmmmmmmmmmh ez")
    await bot.process_commands(ctx)


def is_it_me(ctx):
    return ctx.message.author.id == KEYS.my_id


@client.command()
@commands.check(is_it_me)
async def load(ctx, extension):
    client.load_extension(f"OsuRank.cogs.{extension}")
    print(f"{extension} loaded")

@client.command()
@commands.check(is_it_me)
async def unload(ctx, extension):
    client.unload_extension(f"OsuRank.cogs.{extension}")
    print(f"{extension} unloaded")

@client.command()
@commands.check(is_it_me)
async def reload(ctx, extension):
    client.unload_extension(f"OsuRank.cogs.{extension}")
    client.load_extension(f"OsuRank.cogs.{extension}")
    print(f"{extension} reloaded")


for filename in os.listdir("./OsuRank/cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f"OsuRank.cogs.{filename[:-3]}")

client.run(KEYS.token)