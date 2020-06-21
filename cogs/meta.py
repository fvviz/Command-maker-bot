import discord
from discord.ext import commands
import psutil
import os
class Meta(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def invite(self, ctx):

        embed = discord.Embed(title = f"Click here to invite me to your server",
                              url = "https://discord.com/oauth2/authorize?client_id=717062311755513976&scope=bot&permissions=523336",
                              color = discord.Color.dark_blue())

        embed.description = ":point_up: click on the above link"

        embed.set_thumbnail(url  = self.bot.user.avatar_url)

        await ctx.send(embed= embed)

    @commands.command()
    async def support(self,ctx):
        await ctx.send("https://discord.gg/9zSXyE9")



def setup(bot):
    bot.add_cog(Meta(bot))
