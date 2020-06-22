import dbl
import discord
from discord.ext import commands
import os
from setup import dbltoken
class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken
        self.dbl = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post():
        print("Server count posted successfully")


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        channel = self.bot.get_channel(724508676588699678)
        await channel.send(data)

def setup(bot):
    bot.add_cog(TopGG(bot))