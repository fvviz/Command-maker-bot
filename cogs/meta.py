import discord
from discord.ext import commands
from discord.utils import oauth_url


class Meta(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """
        Sends an invite link
        """

        bot_invite = oauth_url("717062311755513976", discord.Permissions(
            read_messages=True,
            send_messages=True,
            send_tts_messages=True,
            embed_links=True,
            read_message_history=True,
            mention_everyone=True,
            external_emojis=True,
            attach_files=True,
            add_reactions=True,
            manage_messages=True
        ))
        embed = discord.Embed(title = f"Click here to invite me to your server",
                              url = bot_invite,
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
