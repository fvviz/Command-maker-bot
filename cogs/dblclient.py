import dbl
import discord
from discord.ext import commands , tasks
import os
from setup import dbltoken
import logging
import asyncio
from utils.voteLister import Votelister


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken
        self.dbl = dbl.DBLClient(self.bot, self.token, autopost=True)


    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

        # if you are not using the tasks extension, put the line below


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        memberID = data["user"]

        member = self.bot.get_user(int(memberID))
        await member.send(f"""
Hey!Thanks for the vote :heart: :100:
Please do this every now and then :heart:
Enjoy making commands using me!""")

        lister = Votelister()
        lister.add_voter(member)

    @tasks.loop(minutes=10)
    async def clear_voters(self):

        lister = Votelister()
        lister.clear_votes()

        owner = self.bot.get_user(247292930346319872)
        await owner.send("cleared voters")










def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))