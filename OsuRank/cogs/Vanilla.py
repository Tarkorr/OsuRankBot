import discord
from discord.ext import commands
from PycordPaginator import Paginator

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
        embeds = []
        
        embed = discord.Embed(title=f"__commande help :__", color=0xff69b4)
        embed.add_field(name=f"**__liste des commandes:__**",
                        value="",
                        inline=False)
        
        for command in self.client.commands:
            if not command.hidden:
                
                field = embed.fields[0]
                
                if len(field.value) > 900:

                    embeds.append(embed.copy())
                    embed = discord.Embed(title=f"__commande help :__", color=0xff69b4)
                    embed.add_field(name=f"**__liste des commandes:__**",value="",inline=False)
                    field = embed.fields[0]


                if command.aliases:
                    embed.set_field_at(0, name=field.name,
                                    value=field.value + f"**__{command.name} :__** {command.brief}"
                                                        f"\n*__usage :__* `{command.usage}`"
                                                        f"\n*__alias :__* {' '.join(command.aliases)}\n\n", inline=False)
                else:
                    embed.set_field_at(0, name=field.name,
                                    value=field.value + f"**__{command.name} :__** {command.brief}"
                                                        f"\n*__usage :__* `{command.usage}`\n\n",
                                    inline=False)
        if len(embed.fields[0].value) != 0:
            embeds.append(embed.copy())
        
        if len(embeds) > 1:
            e = Paginator(client=self.client.components_manager, embeds=embeds, channel=ctx.channel,
                            only=ctx.author, ctx=ctx, use_select=False)
            return await e.start()
        else:
            return await ctx.send(embed=embeds[0])


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