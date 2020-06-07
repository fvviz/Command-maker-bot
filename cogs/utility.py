from discord.ext import commands
from utils.commandMaker import *
import asyncio
import platform
from discord.ext.commands.cooldowns import BucketType
import datetime
import os

class Utility(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases = ["makecmd"])
    @commands.cooldown(3,3600,BucketType.member)
    async def make(self,ctx,name,*,content):



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

               if len(name) < 12:
                   if name.startswith("@") or name.startswith("<"):
                       await msg.edit(":x: | command names cant start with `@` or `<`")
                   else:

                       await asyncio.sleep(2)
                       await msg.edit(content = f"<:greenTick:596576670815879169> | command **{name}** available ")
                       msg2 = await ctx.send(f"<a:loading:718075868345532466> | creating command **{name}**")


                       commandMaker.create_command(name,ctx.author,await commands.clean_content().convert(ctx,content))

                       await asyncio.sleep(2)

                       await msg2.edit(content = "<:greenTick:596576670815879169>  | command created ")


               else:
                    await msg.edit(content = f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")
















    @make.error
    async def make_error(self,ctx,error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":x: | Only 3 commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds = error.retry_after))[2:4]} minutes**")


        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")



    @commands.command()
    async def clean(self,ctx,arg):

        await ctx.send(await commands.clean_content().convert(ctx,arg))

    @commands.command(aliases = ["commmandauthor"])
    async def commandinfo(self,ctx,command):

        guild = ctx.guild

        try:
            commandMaker = CommandMaker(guild,self.bot)

            authorID = commandMaker.get_command_author_id(command)

            author = guild.get_member(int(authorID))

            embed =  discord.Embed(title=f"{command} command",color=0x36393E)
            embed.set_author(name = author,icon_url=author.avatar_url)

            await ctx.send(embed = embed)
        except:
            await ctx.send("command does not exist?")




    async def has_perms(ctx):

        if ctx.author.id == 247292930346319872:
            return True
        elif ctx.author.guild_permissions.administrator:
            return True

        else:
            return False

    @commands.command(aliases = ["resetcmds","nukeall"])
    @commands.check(has_perms)
    async def nukecommands(self,ctx):
        msg = await ctx.send(f"<a:loading:718075868345532466> | nuking **{ctx.guild.name}** custom commands")
        os.remove(f"data/{ctx.guild.id}.csv")
        await asyncio.sleep(2)
        await msg.edit(content = f"<:greenTick:596576670815879169> | nuked")


    @nukecommands.error
    async def nukecommands_error(self,ctx,error):

        if isinstance(error,commands.CheckFailure):
            await ctx.send("you require `administrator` permissions to execute that command")


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









