from discord.ext import commands
from utils.commandMaker import *
import asyncio
import platform
from discord.ext.commands.cooldowns import BucketType
import datetime
import os
from utils.helperFuncs import *

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["makecmd"])
    @commands.cooldown(3, 3600, BucketType.member)
    async def make(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid make type passed')

    @make.command()
    async def text(self, ctx, name, *, content):
        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/text/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "text")

        commandMaker = CommandMaker('text', guild, self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content=":x: | A command with that name already exists")

        else:

            if len(name) < 12:
                if name.startswith("@") or name.startswith("<"):
                    await msg.edit(":x: | command names cant start with `@` or `<`")
                else:

                    await asyncio.sleep(2)
                    await msg.edit(content=f"<:greenTick:596576670815879169> | command **{name}** available ")
                    msg2 = await ctx.send(f"<a:loading:718075868345532466> | creating command **{name}**")

                    commandMaker.create_text_command(name, ctx.author,
                                                     await commands.clean_content().convert(ctx, content))

                    await asyncio.sleep(2)

                    await msg2.edit(content="<:greenTick:596576670815879169>  | command created ")


            else:
                await msg.edit(
                    content=f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")

    @make.command()
    async def choice(self, ctx, name, *, choices):
        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/choice/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "choice")

        commandMaker = CommandMaker("choice", guild, self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content=":x: | A command with that name already exists")
        else:

            print("made it till here")

            if len(name) < 12:
                if name.startswith("@") or name.startswith("<"):
                    await msg.edit(":x: | command names cant start with `@` or `<`")
                else:
                    await asyncio.sleep(2)
                    await msg.edit(content=f"<:greenTick:596576670815879169> | command **{name}** available ")
                    msg2 = await ctx.send(f"<a:loading:718075868345532466> | creating command **{name}**")

                    choices = await commands.clean_content().convert(ctx, choices)
                    print(choices)
                    choicelist = choices.split(".")

                    if len(choicelist) > 1:

                        commandMaker.make_choice_command(name, ctx.author, choices)
                        await asyncio.sleep(2)
                        await msg2.edit(content=f"<:greenTick:596576670815879169> | command **{name}** created")
                    else:
                        await msg2.edit(content=f":x: | bruh you can't just have one choice , try adding more")

            else:
                await msg.edit(
                    content=f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")


    @make.command(name = "embed")
    async def embed(self,ctx,name,*,description):
        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/choice/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "choice")

        commandMaker = CommandMaker("embed", guild, self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content=":x: | A command with that name already exists")

        else:
            await asyncio.sleep(2)
            await msg.edit(content=f"<:greenTick:596576670815879169> | command **{name}** available ")
            msg2 = await ctx.send(f"<a:loading:718075868345532466> | creating command **{name}**")

            commandMaker.make_embed_command(name,ctx.author,description = description)

            await asyncio.sleep(2)
            await msg2.edit(content=f"<:greenTick:596576670815879169> | command **{name}** created")


    @make.error
    async def make_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

    @text.error
    async def text_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

    """

    @choice.error
    async def choice_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

    """


    @commands.group(name="embed")
    async def edit_embed(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid make type passed')

    @edit_embed.command()
    async def setcolor(self,ctx,name,*,color):
        guild = ctx.guild
        commandMaker = CommandMaker("embed", guild, self.bot)

        if commandMaker.embed_command_exists(name):
            if does_color_exist(color):
                     msg2 = await ctx.send(f"<a:loading:718075868345532466> | setting color of embed command **{name}** to `{color}`")
                     commandMaker.modfiy_embed_color(ctx.author, name, color)

                     await ctx.send("modfied")

                     await asyncio.sleep(2)
                     await msg2.edit(content=f"<:greenTick:596576670815879169> | changed color of embed command **{name}** to {color}")
            else:



                colors = ""
                for color in color_dict.keys():
                    colors += f"`{color}` "

                await ctx.send(f"that color does not seem to exist, the available colors are {colors}")

    @edit_embed.command()
    async def addtitle(self, ctx, name, *, title):
        guild = ctx.guild
        commandMaker = CommandMaker("embed", guild, self.bot)

        if commandMaker.embed_command_exists(name):

            if len(title) < 256:

                msg2 = await ctx.send(
                    f"<a:loading:718075868345532466> | setting title of embed command **{name}**")
                commandMaker.add_title(ctx.author, name, title)
                await asyncio.sleep(2)
                await msg2.edit(
                    content=f"<:greenTick:596576670815879169> | title of embed command**{name}** has been set")

        else:

            await ctx.send("too bad , command does not seem to exist , make the command first and then add titles using this command")

    @commands.command(aliases=["commmandauthor"])
    async def commandinfo(self, ctx, command):

        guild = ctx.guild

        try:
            commandMaker = CommandMaker(guild, self.bot)

            authorID = commandMaker.get_command_author_id(command)

            author = guild.get_member(int(authorID))

            embed = discord.Embed(title=f"{command} command", color=0x36393E)
            embed.set_author(name=author, icon_url=author.avatar_url)

            await ctx.send(embed=embed)
        except:
            await ctx.send("command does not exist?")

    async def has_perms(ctx):

        if ctx.author.id == 247292930346319872:
            return True
        elif ctx.author.guild_permissions.administrator:
            return True

        else:
            return False

    @commands.command(aliases=["resetcmds", "nukeall"])
    @commands.check(has_perms)
    async def nukecommands(self, ctx):
        msg = await ctx.send(f"<a:loading:718075868345532466> | nuking **{ctx.guild.name}** custom commands")
        os.remove(f"data/{ctx.guild.id}.csv")
        await asyncio.sleep(2)
        await msg.edit(content=f"<:greenTick:596576670815879169> | nuked")

    @nukecommands.error
    async def nukecommands_error(self, ctx, error):

        if isinstance(error, commands.CheckFailure):
            await ctx.send("you require `administrator` permissions to execute that command")

    @commands.command(aliases=["deletecmd", "remove"])
    async def delete(self, ctx, command):

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
    async def run(self, ctx, name):

            print(ctx.message.content)
            try:
                commandMaker = CommandMaker("text", ctx.guild, self.bot)
                output = commandMaker.run_text_command(name)
                await ctx.send(output)
            except Exception:

                print(f"{Exception}")

                try:
                    commandMaker = CommandMaker("choice", ctx.guild, self.bot)
                    output = commandMaker.run_choice_command(name)
                    await ctx.send(output)
                except Exception:
                    print(f"{Exception}")
                    commandMaker = CommandMaker("embed", ctx.guild, self.bot)
                    output = commandMaker.run_embed_command(name)
                    await ctx.send(embed = output)




    @commands.command()
    async def edit(self, ctx, name):

        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"data/text/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild=guild,type="text")
        commandMaker = CommandMaker("text",guild, self.bot)

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
                await newmsg.edit(content="<:greenTick:596576670815879169> | **checks completed**")
                newmsg2 = await ctx.send(f"<a:loading:718075868345532466> | **editing command** `{name}`")
                await asyncio.sleep(2)
                await newmsg2.edit(
                    content=f"<:greenTick:596576670815879169> | **command `{name}` edited successfully**")

            except Exception as error:
                await asyncio.sleep(2)
                await newmsg.edit(content=f":x: | **checks failed** : `{error}`")

        elif commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await msg.edit(content=f":x: | **Nice try , But Built-in utility commands cannot be edited**")

        else:
            await asyncio.sleep(2)
            await msg.edit(content=f":x: | **Command does not exist**")

    @commands.command(aliases=["showcommands", "cmds"])
    async def commands(self, ctx):

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
        cmds2 = ""

        for command in commandlist1:
            cmds1 += f"`{command}` "

        for command in commandlist2:
            cmds2 += f"`{command}` "

        embed = discord.Embed(
            description=f"""
**__{ctx.guild.name} command list__**

**📝 Text commands**
{cmds1}

**📝 Choice commands**
{cmds2}
                                           """,
            color=discord.Color.dark_blue())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))



