import dbl
from discord.ext import commands
from setup import dbltoken,dblauth
import logging
from utils.tokenMaker import TokenMaker


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken
        self.auth = dblauth
        self.dblpy = dbl.DBLClient(self.bot,
                                   self.token,
                                   webhook_path='/dblwebhook',
                                   webhook_auth=dblauth,
                                   webhook_port=5000)




    @commands.Cog.listener()
    async def on_dbl_test(self, data):

        testing = self.bot.get_channel(712639566774796298)
        await testing.send("tested")
        print("TESTED")
        print(data)


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        memberID = data["user"]

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