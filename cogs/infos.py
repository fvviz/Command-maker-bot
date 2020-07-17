import discord
from discord.ext import commands
from utils.commandMaker import *
from utils.permsHandler import PermsHandler
from utils.helperFuncs import *
import platform
import psutil
import git
class Info(commands.Cog):

    """
    Informational commands
    """

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="command-list", aliases=["showcommands", "cmds"])
    async def _commands(self, ctx):

        guild = ctx.guild

        try:
            pd.read_csv(f"data/text/{guild.id}.csv")

            try:
                pd.read_csv(f"data/choice/{guild.id}.csv")

            except FileNotFoundError:
                make_csv(guild, "choice")

        except FileNotFoundError:
            make_csv(guild, "text")

        commandMaker = CommandMaker("text", guild, self.bot)

        commandlist1 = commandMaker.text_commands
        cmds1 = ""

        commandlist2 = commandMaker.choice_commands
        commandlist3 = commandMaker.embed_commands
        commandlist4 = commandMaker.ce_commands
        commandlist5 = commandMaker.rate_commands

        cmds3 = ""
        cmds2 = ""
        cmds4 = ""
        cmds5 = ""

        for command in commandlist1:
            cmds1 += f"`{command}` "

        for command in commandlist2:
            cmds2 += f"`{command}` "

        for command in commandlist3:
            cmds3 += f"`{command}` "

        for command in commandlist4:
            cmds4 += f"`{command}` "

        for command in commandlist5:
            cmds5 += f"`{command}` "

        embed = discord.Embed(
            description=f"""
    **__{ctx.guild.name} command list__**

    **📝 Text commands**
    {cmds1}

    **📝 Choice commands**
    {cmds2}

    **📝 Embed(v1) commands**
    {cmds3}

    **📝 Embed(v2) commands**
    {cmds4}

    **📝 Rate commands**
    {cmds5}

                                               """,
            color=discord.Color.dark_blue())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def settings(self, ctx):

        embed = discord.Embed(color=0x36393E)

        embed.set_author(name=f"settings for {ctx.guild.name}", icon_url=ctx.guild.icon_url)

        ph = PermsHandler(ctx.guild)

        message = format_rr_message(ctx, ph)

        content = ""

        embed.description = f"""

            **Role Restrictions** : {bool_to_em(ph.has_perms_role())}\n{message}
            **Welcome message**  : {bool_to_em(False)}


            """

        await ctx.send(embed=embed)

    @commands.command(aliases = ["botinfo"])
    async def about(self,ctx):


        embed = discord.Embed(color=discord.Color.dark_blue())

        owner = self.bot.get_user(247292930346319872)

        embed.set_author(name=f"Developer : {owner}",icon_url=owner.avatar_url)
        embed.description = """ 
        **Command maker** is a discord bot with which you can make your own simple commands.
        """
        versions = f"<:python:596577462335307777> Python {platform.python_version()}\n<:dpy:596577034537402378> discord.py {discord.__version__}"
        links = f"""

<:discord:314003252830011395> [**Support Server**](
https://discord.gg/vfvyjDA)
<a:dblspin:393548363879940108> [**Vote**](
https://discord.gg/vfvyjDA)
<:github:727808408203558952> [**Source**](https://github.com/fwizzz/Command-maker-bot)

"""

        system = f"""
CPU Usage   :`{psutil.cpu_percent()}%`
Memory used :`{bytes_format(psutil.virtual_memory().used)}/{bytes_format(psutil.virtual_memory().total)}`
"""

        counts = f"""
🏘️ Servers : {len(self.bot.guilds)}
<:user:727539132099723335> Users   : {len(self.bot.users)}

"""

        total, file_amount = linecount()

        code = f"""
📁 {file_amount} files
<:vscode:727802262981836880> {total} lines

"""





        embed.add_field(name="Versions",value=versions)
        embed.add_field(name="Links",value=links)
        embed.add_field(name="System",value=system)
        embed.add_field(name="Counts",value=counts)
        embed.add_field(name="Code",value=code)
        embed.add_field(name="Development Status",value="Currently under development")
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        embed.title = "Bot info"
        embed.url = "https://docs.command-maker.ml/"


        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))

