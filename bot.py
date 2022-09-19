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
    if ctx.channel.id == 966475432998338590 and ctx.attachments == []:
        await ctx.author.send(
            "*(Mr. ORB727-Manager enters as the player leaves home, popping out of the ground.)*"
            "\nHello. Um...allow me to introduce myself. The name's __OsuRankBot__. __Mr. OsuRankBot.__"
            "\nHave we...met before? At the... <#871482413191139338> channel, perhaps? Yeah, whatever."
            "\n\nAnyway, let me just say thanks for using me, whenever you want to show of your skill."
            "\nUm...on behalf of everyone at *__Tarkor Industries__*, I...um...I..."
            "\nWhat was the next part? Huh? Aw, forget it! That's enough!"
            "\nLet's get down to business, whaddaya say? Because you may not know it, but you and I got issues to discuss."
            "\nFirst, let me just tell you what it is I'm doin' here. Just so there are no misunderstandings later on."
            "\nYou, my friend, **SENT A MESSAGE** in <#966475432998338590>, didn't you? Huh? Maybe on accident, maybe on purpose, but you sent it."
            "\nOr maybe you didn't, huh? Maybe you just went and a friend did it for you. Sound familiar?"
            "\nWhat? Sorry, what was that? I didn't catch that last bit. Did you just say **I**'m right? You did what I said you did?"
            "\n**Ah-HAH!!!**"
            "\n\nAll right, you **LISTEN** and **LISTEN** good, 'cause I get real angry when I gotta repeat stuff I gotta say."
            "\n***Sending Messages in <#966475432998338590>***... It's like...pressing an emergency call button. You press it and I gotta come read you the riot act. See?"
            "\nAlso, you gotta **TALK somewhere else**. If you don't, *it's the same as kiling a kitten with your bare hands.*"
            "\nWell, OK... That last part? I just added that. Why? *Because I wanted to.*"
            "\nForget about other Bots for a minute, will ya?")
        await ctx.author.send(
            "\n\nI'm here to suggest that you try and use **THIS** bot, OsuRankBot, ***without sending messages in <#966475432998338590>.*** Got it?"
            "\nI know what you're thinking: 'Whether I send a **MESSAGE** or not should be up to me. After all, it's **MY DISCORD!**'"
            "\nWell, sorry. Rules are rules, OK? Know what I'm sayin'? Let's not make a big deal out of this. End of discussion. +ratio this is **MY** server, even tho I may not have the crown, I have big perms."
            "\nThis bein' our first meeting, I'm gonna let you off easy. Think of this as a friendly warning from me to you."
            "\nOh, one more thing. This is my job. I take it seriously. So next time you see me, it's no more Mr. Nice Bot."
            "\n\nOh, yeah, and another thing I guess I gotta say here..."
            "\nI really watched my... language...here today. I'm not usually quite so... you know, so polite."
            "\nIf I'm bein' truthful here, I gotta tell you... I been told I got what you call an acid tongue. I sorta...scare people."
            "\nHey, that's...who I am. Nothin' I can do about it. What, I'm supposed to say sorry for bein' me?"
            "\nLook, it's nothin' personal. I ain't tryin' to be mean or cruel or nothin'. I ain't a monster."
            "\nFor those people who get their feelin's bruised easily, I gotta apologize in advance. Just deal with it, OK?"
            "\nThe deal is, I get paid to be nasty. Crazy world, huh? Ha ha ha ha ha!!!"
            "\nWell, I figure it's about time for me to get outta here."
            "\nSo, uh... Yeah. Here's hoping I don't have to come see you no more. Now..."
            "\nSCRAM!"
            "\n\n*(ORB727-Manager burrows back into the ground.)*")
        await ctx.delete()
        
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
    await client.process_commands(ctx)


def is_it_me(ctx):
    return ctx.message.author.id == KEYS.my_id


@client.command(name="load",
             brief="Charge un cog.",
             hidden=True
             )
@commands.check(is_it_me)
async def load(ctx, extension):
    try:
        client.load_extension(f"OsuRank.cogs.{extension}")
    except discord.ext.commands.errors.ExtensionAlreadyLoaded as e:
        print(e)
        return await ctx.send(e)
    await ctx.send(f"{extension} loaded." \
                   f"\n{', '.join([c for c in client.cogs])} are currently loaded cogs.")
    print(f"{extension} loaded." \
          f"{', '.join([c for c in client.cogs])} are currently loaded cogs.")

@client.command(name="unload",
             brief="Décharge un cog.",
             hidden=True
             )
@commands.check(is_it_me)
async def unload(ctx, extension):
    try:
        client.unload_extension(f"OsuRank.cogs.{extension}")
    except discord.ext.commands.errors.ExtensionNotLoaded as e:
        print(e)
        return await ctx.send(e)
    await ctx.send(f"{extension} unloaded." \
                   f"\n{', '.join([c for c in client.cogs])} are currently loaded cogs.")
    print(f"{extension} unloaded." \
          f"{', '.join([c for c in client.cogs])} are currently loaded cogs.")


@client.command(name="reload",
             brief="recharge un cog.",
             hidden=True
             )
@commands.check(is_it_me)
async def reload(ctx, extension):
    try:
        client.unload_extension(f"OsuRank.cogs.{extension}")
        client.load_extension(f"OsuRank.cogs.{extension}")
    except (commands.ExtensionNotLoaded, commands.ExtensionAlreadyLoaded) as e:
        print(e)
        return await ctx.send(e)
    await ctx.send(f"{extension} reloaded.")
    print(f"{extension} reloaded.")


for filename in os.listdir("./OsuRank/cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f"OsuRank.cogs.{filename[:-3]}")

client.run(KEYS.token)