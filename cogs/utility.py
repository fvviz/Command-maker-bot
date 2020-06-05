from discord.ext import commands
from utils.commandMaker import *
import asyncio
import platform

class Utility(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases = ["makecmd"])
    async def make(self,ctx,name):

        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild)

        commandMaker = CommandMaker(guild,self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content = ":x: | A command with that name already exists")

        else:

            await asyncio.sleep(2)
            await msg.edit(content = f"<:greenTick:596576670815879169> | command **{name}** available ")

            await ctx.send("Now , please type out the output of the command, **You have 20 seconds**")

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            content = await self.bot.wait_for("message",check = check)

            commandMaker.create_command(name,ctx.author,content.content)

            await ctx.send("<:greenTick:596576670815879169>  | command created ")


    @commands.command(aliases = ["deletecmd","remove"])
    async def delete(self,ctx,command):

        guild = ctx.guild

        try:

            commandMaker = CommandMaker(guild, self.bot)

            if command in commandMaker.commands:

                try:
                    commandMaker.delete_command(ctx.author, command)
                    msg = await ctx.send(f"<a:loading:718075868345532466> | Removing command `{command}`")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"<:greenTick:596576670815879169> | Removed command {command} ")

                except:
                    await ctx.send(":x: | **You are not the owner of that command**")






            else:
                await ctx.send(":x: | **Command does not exist**")


        except FileNotFoundError:
            make_csv(guild)


    @commands.command()
    async def edit(self,ctx,name):

        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild)

        commandMaker = CommandMaker(guild, self.bot)

        if commandMaker.custom_command_exists(name):
            await asyncio.sleep(2)

            await msg.edit(content=f"<:greenTick:596576670815879169> | command **{name}** exists")


            await ctx.send("Now , please type out the output of the command, **You have 20 seconds**")

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            content = await self.bot.wait_for("message", check=check)

            try:
                newmsg = await ctx.send("<a:loading:718075868345532466> | **running checks**")
                commandMaker.edit_command(name, ctx.author, content.content)
                await asyncio.sleep(2)
                await newmsg.edit(content = "<:greenTick:596576670815879169> | **checks completed**")
                newmsg2 = await ctx.send(f"<a:loading:718075868345532466> | **editing command** `{name}`")
                await asyncio.sleep(2)
                await newmsg2.edit(content = f"<:greenTick:596576670815879169> | **command `{name}` edited successfully**")

            except Exception as error:
                await asyncio.sleep(2)
                await newmsg.edit(content=f":x: | **checks failed** : `{error}`")

        elif commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content = f":x: | **Nice try , But Built-in utility commands cannot be edited**")

        else:
            await asyncio.sleep(2)
            await msg.edit(content=f":x: | **Command does not exist**")








    @commands.command(aliases = ["showcommands","cmds"])
    async def commands(self,ctx):

        guild = ctx.guild

        try:
            pd.read_csv(f"data/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild)

        commandMaker = CommandMaker(guild,self.bot)

        commandlist = commandMaker.commandlist
        cmds = ""

        for command in commandlist:
            cmds += f"`{command}` "
        embed = discord.Embed(
                              description=f"**__{ctx.guild.name} command list__**"
                                          f"\n\n{cmds}",
                              color= discord.Color.dark_blue())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)




def setup(bot):
   bot.add_cog(Utility(bot))









