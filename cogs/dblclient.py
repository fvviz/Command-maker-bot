import dbl
from discord.ext import commands , tasks
from setup import dbltoken,dblauth
import logging
from utils.tokenMaker import TokenMaker
from utils.voteHandler import VoteHandler
import discord
from datetime import datetime



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


        async def get_supporters():

            await bot.wait_until_ready()

            guild = bot.get_guild(581084433646616576)

            role = guild.get_role(724522070960111626)
            supporters = []

            for member in guild.members:
                if role in member.roles:
                    supporters.append(member)

            self.supporters = supporters
        bot.loop.create_task(get_supporters())







    @commands.Cog.listener()
    async def on_dbl_test(self, data):

        memberID = data["user"]

        user = self.bot.get_user(int(memberID))
        msg = await user.send(f"""
Hey! Thanks for the vote :heart: :100:
You now have one extra token :moneybag: 
Please do this every now and then :heart:
Enjoy making commands using me!""")

        channel = self.bot.get_channel(724508676588699678)
        guild = channel.guild

        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_author(name=f"{user} just voted",icon_url=user.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/376811626197811200.png?v=1")

        if user in guild.members:

            vh = VoteHandler(user)
            vh.add_vote(msg.created_at)

            embed.description = f"""
        {user.mention} You now have the supporter role for 12 hours
        and you've gained an extra token :moneybag:!.
        """

            role = guild.get_role(724522070960111626)
            member = guild.get_member(user.id)
            print(member)
            await member.add_roles(role)

        else:
            embed.description = "User is not in this server"

        embed.set_footer(text="Discord Bot list",
                         icon_url="https://cdn.discordapp.com/emojis/393548388664082444.gif?v=1")

        await channel.send(embed=embed)

        tokenmaker = TokenMaker(user)
        tokenmaker.add_token()


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        memberID = data["user"]

        user = self.bot.get_user(int(memberID))
        msg = await user.send(f"""
Hey! Thanks for the vote :heart: :100:
You now have one extra token :moneybag: 
Please do this every now and then :heart:
Enjoy making commands using me!""")

        channel = self.bot.get_channel(724508676588699678)
        guild = channel.guild

        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_author(name=f"{user} just voted", icon_url=user.avatar_url)

        if user in guild.members:

            vh = VoteHandler(user)
            vh.add_vote(msg.created_at)

            embed.description = f"""
{user.mention} You now have the supporter role for 12 hours
and you've gained an extra token :moneybag:
                """

            role = guild.get_role(724522070960111626)
            member = guild.get_member(user.id)
            print(member)
            await member.add_roles(role)

        else:
            embed.description = "User is not in this server"

        embed.set_footer(text="Discord Bot list",
                         icon_url="https://cdn.discordapp.com/emojis/393548388664082444.gif?v=1")

        await channel.send(embed=embed)

        tokenmaker = TokenMaker(user)
        tokenmaker.add_token()


    @tasks.loop(minutes = 5)
    async def check_support(self):

        supporters = self.supporters

        guild = self.bot.get_guild(581084433646616576)
        role = guild.get_role(724522070960111626)

        for member in supporters:
            vh = VoteHandler(member)
            now = datetime.now()
            vote_time = datetime.fromtimestamp(vh.get_stamp())

            time_delta = vote_time - now

            hours = time_delta.total_seconds()/3600

            if hours > 12:
                await member.remove_roles(role)
            else:
                pass


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