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

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def massmessage(self, ctx):

        author = self.bot.get_user(247292930346319872)

        message = """
Bot is currently under maintenance, Some of the data is currently unavailable (saved prefixes, commands).
The bot is being moved to another Server. So this can take a few hours.
All the data can possibly be back in a few more hours

Thank you for your patience.
        
        """

        embed = discord.Embed(title = "Important notice from the developer",
                              description= message,
                              color = discord.Color.blue())

        embed.set_author(name = author.name , icon_url= author.avatar_url)

        success = []
        failures = []
        for guild in self.bot.guilds:
            try:
                await guild.system_channel.send(embed = embed)

                success.append(guild.name)

            except:
                channels = guild.channels

                m = 0

                for channel in channels:

                    if m == 0:
                       try:

                           await channel.send(embed = embed)

                           m = 1

                           success.append(guild.name)

                       except:

                           failures.append(guild.name)

                await ctx.send(f"""
                
{len(success)} successful
{len(failures)} failures              
                """)














def setup(bot):
    bot.add_cog(BotOwner(bot))