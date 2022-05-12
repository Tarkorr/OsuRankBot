import discord
from discord.ext import commands

prefix = "!o "

class Vanilla(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def test(self, ctx):
        await ctx.send('test !')

    @commands.command(name="hlp",
             brief="comme son nom l'indique.",
             usage=f"{prefix}hlp",
             hidden=True)
    async def hlp(self, ctx):
        print(f"commande 'help' éxécuté par {ctx.author}")
        embed = discord.Embed(title=f"__commande help :__", color=0xff69b4)
        embed.add_field(name=f"**__liste des commandes:__**",
                        value="",
                        inline=False)
        for command in self.client.commands:
            if not command.hidden:
                index = len(embed.fields) - 1
                field = embed.fields[index]
                if len(field.value) > 900:
                    embed.add_field(name="═" * 20 + f"> {index + 1} <" + "═" * 20,
                                    value="",
                                    inline=False)

                field = embed.fields[len(embed.fields) - 1]

                if command.aliases:
                    embed.set_field_at(len(embed.fields) - 1, name=field.name,
                                    value=field.value + f"**__{command.name} :__** {command.brief}"
                                                        f"\n*__usage :__* `{command.usage}`"
                                                        f"\n*__alias :__* {' '.join(command.aliases)}\n\n", inline=False)
                else:
                    embed.set_field_at(len(embed.fields) - 1, name=field.name,
                                    value=field.value + f"**__{command.name} :__** {command.brief}"
                                                        f"\n*__usage :__* `{command.usage}`\n\n",
                                    inline=False)
        await ctx.send(embed=embed)


    @commands.command(name="ban",
             usage=f"{prefix}ban <id>",
             brief="ban une personne via son id.",
             hidden=True
             )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, id: int):
        print(f"commande 'ban' éxécuté par {ctx.author}")
        user = await self.client.fetch_user(id)
        await ctx.guild.ban(user)
        await ctx.send(f"{ctx.author}, a ban {user}")

    
    @commands.command(name="ping",
             usage=f"{prefix}ping",
             brief="permet de ping le bot pour connaître son temps de réaction si >2ms dm Tarkor."
             )
    async def ping(self, ctx):
        print(f"commande 'ping' éxécuté par {ctx.author}")
        await ctx.send(f"pong with {round(self.client.latency)} ms", file=discord.File("pong.png"))

    
    @commands.command(name="clear",
    usage=f"{prefix}clear <amount>",
    alias=["prune", "purge"],
    brief="permet de supprimer rapidement un certain nombre de messages."
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        print(f"commande 'clear' éxécuté par {ctx.author}")
        return await ctx.channel.purge(limit=amount+1)


def setup(client):
    client.add_cog(Vanilla(client))