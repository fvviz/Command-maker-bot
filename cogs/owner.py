from discord.ext import commands
import discord
import asyncio
import math



class BotOwner(commands.Cog):
    """Shows help for bot"""

    def __init__(self, bot):
        self.bot = bot

    async def is_owner(ctx):
        return ctx.author.id == 247292930346319872

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def show_guilds(self,ctx):
        text = ""

        for i in self.bot.guilds:
            text += f"\n {i.name}"
        await ctx.send(text)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def leave_guild(self,ctx, *, guildname):
        for guild in self.bot.guilds:
            if guild.name == guildname:
                await ctx.message.add_reaction("<:greenTick:596576670815879169>")
                await guild.leave()

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def show_cogs(self,ctx):
        text = ""

        for i in self.bot.cogs:
            cog = self.bot.get_cog(i)
            text += f"\n {cog.qualified_name}"
        await ctx.send(text)


def setup(bot):
    bot.add_cog(BotOwner(bot))