from discord.ext import commands
import discord
from utils.tokenMaker import TokenMaker
from utils.voteHandler import VoteHandler

class BotOwner(commands.Cog):
    """Shows help for bot"""

    def __init__(self, bot):
        self.bot = bot

    async def is_owner(ctx):
        return ctx.author.id == 247292930346319872 or ctx.author.id == 392686296860065792 or ctx.author.id == 303049066525491201

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

    @commands.command(hidden = True)
    @commands.check(is_owner)
    async def add_token(self,ctx,member : discord.Member):

        tm = TokenMaker(member=member)
        tm.add_token()

        await ctx.send("done")

    @commands.command(hidden = True)
    @commands.check(is_owner)
    async def add_voter(self,ctx,member:discord.Member):

         vh = VoteHandler(member)
         msg = await ctx.send("ok")
         vh.add_vote(msg.created_at)
         await ctx.send('done')

















def setup(bot):
    bot.add_cog(BotOwner(bot))