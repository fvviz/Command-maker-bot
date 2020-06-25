import dbl
from discord.ext import commands
from setup import dbltoken
import logging
from utils.tokenMaker import TokenMaker

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken
        self.dblpy = dbl.DBLClient(self.bot,
                                   self.token,
                                   webhook_path='/dblwebhook',
                                   webhook_auth='loliamtesting',
                                   webhook_port=5000)



        # if you are not using the tasks extension, put the line below

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        print("vote testing")

        memberID = data["user"]

        print(f"got vote from {memberID}")

        member = self.bot.get_user(int(memberID))
        print(member.name)
        await member.send(f"""
Hey!Thanks for the vote :heart: :100:
You now have one extra token :moneybag: 
Please do this every now and then :heart:
Enjoy making commands using me!""")

        tokenmaker = TokenMaker(member)
        tokenmaker.add_token()


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.dblpy.post_guild_count()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.dblpy.post_guild_count()




def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))