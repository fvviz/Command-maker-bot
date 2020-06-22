import discord
from discord.ext import commands
import psutil
import os
class Meta(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):

        embed = discord.Embed(title = f"Click here to invite me to your server",
                              url = "https://discord.com/oauth2/authorize?client_id=717062311755513976&scope=bot&permissions=523336",
                              color = discord.Color.dark_blue())

        embed.set_thumbnail(url  = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(name  = "support-server")
    async def support_server(self, ctx):
        await ctx.send("https://discord.gg/vfvyjDA")

    @commands.command()
    async def vote(self,ctx):
        await ctx.send("https://top.gg/bot/717062311755513976/vote")


def setup(bot):
    bot.add_cog(Meta(bot))
