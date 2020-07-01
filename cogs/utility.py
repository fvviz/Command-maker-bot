from utils.commandMaker import *
import asyncio
from discord.ext.commands.cooldowns import BucketType
import os
from utils.helperFuncs import *
import requests
from bot import prefix
from utils.prefixMaker import PrefixHandler
from utils.tokenMaker import TokenMaker
from utils.runner import exec
from utils.permsHandler import PermsHandler


tick = "<:greenTick:596576670815879169>"

class Utility(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    def has_cm_perms(ctx):
        ph = PermsHandler(ctx.guild)
        return ph.has_perms(ctx.author,ctx.bot)

    @commands.group(aliases=["makecmd"])
    @commands.check(has_cm_perms)
    async def make(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title = "Making command",
                                  color = discord.Color.dark_blue(),url="https://docs.command-maker.ml/")
            embed.description = f"""
To make a command , 
use `{prefix}make <command-type><command-name>`

:pencil: **__Available Command Types__**

Click on a particular command type 
to learn more about it
• [`text`](https://docs.command-maker.ml/command-types/text-commands)
• [`choice`](https://docs.command-maker.ml/command-types/choice-commands)
• [`embed`](https://docs.command-maker.ml/command-types/embed-commands)

For a step by step guide on making commands
[`Click here`](https://docs.command-maker.ml/)


"""
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            await ctx.send(embed = embed)

    @make.command(cooldown_after_parsing = True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def text(self, ctx, name, *, content):
        guild = ctx.guild


        try:
            pd.read_csv(f"{folder}/text/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "text")

        commandMaker = CommandMaker('text', guild, self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await ctx.send(":x: | A command with that name already exists")

        else:

            if len(name) < 12:
                if name.startswith("@") or name.startswith("<"):
                    await ctx.send(":x: | command names cant start with `@` or `<`")
                else:

                    await ctx.send(f"<:greenTick:596576670815879169> | command **{name}** available ",delete_after = 5)
                    commandMaker.create_text_command(name, ctx.author,
                                                     await commands.clean_content().convert(ctx, content))


                    await ctx.send(content="<:greenTick:596576670815879169>  | command created ")


            else:
                await ctx.send(
                    content=f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")

    @make.command(cooldown_after_parsing = True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def choice(self, ctx, name, *, choices):
        guild = ctx.guild

        try:
            pd.read_csv(f"{folder}/choice/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "choice")

        commandMaker = CommandMaker("choice", guild, self.bot)

        if commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await ctx.send(":x: | A command with that name already exists")
        else:

            print("made it till here")

            if len(name) < 12:
                if name.startswith("@") or name.startswith("<"):
                    await ctx.send(":x: | command names cant start with `@` or `<`")
                else:
                    await asyncio.sleep(2)
                    await ctx.send(f"<:greenTick:596576670815879169> | command **{name}** available ")

                    if "/" in choices:
                        choices = await commands.clean_content().convert(ctx, choices)
                        print(choices)
                        choicelist = choices.split("/")

                        if len(choicelist) > 1:

                            commandMaker.make_choice_command(name, ctx.author, choices)
                            await ctx.send(f"<:greenTick:596576670815879169> | command **{name}** created")
                        else:
                            await ctx.send(content=f":x: | bruh you can't just have one choice , try adding more")

                    else:
                        await ctx.send("Choices must be separated by / ,To learn more about choice commands head over to \nhttps://docs.command-maker.ml/command-types/choice-commands")

            else:
                        await ctx.send(f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")


    @make.command()
    async def embed(self,ctx,name,*,code):

        guild = ctx.guild
        try:
            pd.read_csv(f"{folder}/ce/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "ce")

        commandMaker = CommandMaker('ce', guild, self.bot)

        if commandMaker.does_command_exist(name):
            await ctx.send(":x: | A command with that name already exists")

        else:

            if len(name) < 12:
                if name.startswith("@") or name.startswith("{"):
                    await ctx.send(":x: | command names cant start with `@` or `{`")
                else:

                        await ctx.send(f"<:greenTick:596576670815879169> | command **{name}** available ", delete_after=5)


                        try:
                            ec = json.loads(code)

                            check_dict = check_embed(ec)

                            if not check_dict["author_icon"]:
                                await ctx.send("the provided url for author icon did not seem to be a valid image")
                            if not check_dict["image"]:
                                await ctx.send("the provided url for image did not seem to be a valid image")

                            if not check_dict["thumbnail"]:
                                await ctx.send("the provided url for thumbnail did not seem to be a valid image")

                            if not check_dict["footer_icon"]:
                                await ctx.send("the provided url for footer icon did not seem to be a valid image")

                            else:
                                commandMaker.create_ce_command(name, ctx.author, code)
                                await ctx.send(content="<:greenTick:596576670815879169>  | command created ")


                        except ValueError:
                            await ctx.send(f"the provided code does not seem to be valid : `{ValueError}`")


    @make.error
    async def make_error(self, ctx, error):


        if isinstance(error,commands.CheckFailure):

            ph = PermsHandler(ctx.guild)
            role_id = ph.get_role()
            role_name = ctx.guild.get_role(role_id).name
            await ctx.send(f"{ctx.author.mention} you are missing `{role_name}` role to make commands")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

    @text.error
    async def text_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):

            tokenmaker = TokenMaker(ctx.author)

            await reset_timer(ctx = ctx,command_name="make text",bot=self.bot,tokenmaker=tokenmaker,error = error,rate_limit=3)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

    @choice.error
    async def choice_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            tokenmaker = TokenMaker(ctx.author)

            await reset_timer(ctx = ctx,
                              command_name="make text",
                              bot = self.bot,
                              tokenmaker=tokenmaker,
                              error = error,
                              rate_limit=  3)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")


    @commands.group()
    #@commands.cooldown(3, 3600, BucketType.member)
    async def edit(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Editing commands",
                                  color=discord.Color.dark_blue(),
                                  url = "https://docs.command-maker.ml/")

            embed.description = f"""To edit a command,
use {prefix}edit <command-type> <content>

:pencil: **__Available Command Types__**
Click on a particular command type 
to learn more about it

• [`text`](https://docs.command-maker.ml/command-types/text-commands#editing-text-commands)
• [`choice`](https://docs.command-maker.ml/command-types/choice-commands#making-choice-commands)
• [`embed`](https://docs.command-maker.ml/command-types/embed-commands)

For a step by step guide on making commands
[`Click here`](https://docs.command-maker.ml/) 



"""
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed = embed)


    @edit.error
    async def edit_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be edited in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

        if isinstance(error,commands.CommandInvokeError):

            if str(error.original) == "You are not the owner of that command":
                await ctx.send(":x: | you don't seem to be the owner of that command")


    @edit.command(name = "text",cooldown_after_parsing = True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def text_edit(self,ctx,name,*,content):
        guild = ctx.guild

        msg = await ctx.send(f"<a:loading:718075868345532466> | Checking availability of command  `{name}`")
        try:
            pd.read_csv(f"{folder}/text/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild=guild, type="text")
        commandMaker = CommandMaker("text", guild, self.bot)

        if commandMaker.custom_command_exists(name):
            await asyncio.sleep(2)

            await msg.edit(content=f"<:greenTick:596576670815879169> | command **{name}** exists")


            try:
                newmsg = await ctx.send("<a:loading:718075868345532466> | **running checks**")
                commandMaker.edit_command(name, ctx.author, content)
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

    @text_edit.error
    async def text_edit_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be edited in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"bruh you aint even specifying {error.param}")

        if isinstance(error,commands.CommandInvokeError):

            if str(error.original) == "You are not the owner of that command":
                await ctx.send(":x: | you don't seem to be the owner of that command")

    @commands.command()
    async def simple_embed(self, ctx, *, code):
        print(code)

        try:

            embed_code = json.loads(code)
            embed = discord.Embed.from_dict(embed_code)
            await ctx.send(embed=embed)

        except ValueError:
            print("error")

    @commands.command(aliases=["commmandauthor"])
    async def commandinfo(self, ctx, command):

        guild = ctx.guild
        author = ""

        try:

            try:
                commandMaker = CommandMaker("text", guild, self.bot)

                authorID = commandMaker.get_command_author_id(command)

                author = guild.get_member(int(authorID))

                embed = discord.Embed(title=f"{command} command", color=0x36393E)
                embed.set_author(name=author, icon_url=author.avatar_url)
                embed.add_field(name=":pencil: Type", value="text")

                await ctx.send(embed=embed)

            except:

                try:
                    commandMaker = CommandMaker("choice", guild, self.bot)

                    authorID = commandMaker.get_command_author_id(command)

                    author = guild.get_member(int(authorID))

                    embed = discord.Embed(title=f"{command} command", color=0x36393E)
                    embed.set_author(name=author, icon_url=author.avatar_url)
                    embed.add_field(name=":pencil: Type", value="choice")




                    await ctx.send(embed=embed)
                except:

                    try:
                        commandMaker = CommandMaker("embed", guild, self.bot)

                        authorID = commandMaker.get_command_author_id(command)

                        author = guild.get_member(int(authorID))

                        embed = discord.Embed(title=f"{command} command", color=0x36393E)
                        embed.set_author(name=author, icon_url=author.avatar_url)
                        embed.add_field(name=":pencil: Type", value="embed v1")

                        await ctx.send(embed=embed)
                    except:
                        commandMaker = CommandMaker("ce", guild, self.bot)

                        authorID = commandMaker.get_command_author_id(command)

                        author = guild.get_member(int(authorID))

                        embed = discord.Embed(title=f"{command} command", color=0x36393E)
                        embed.set_author(name=author, icon_url=author.avatar_url)
                        embed.add_field(name=":pencil: Type", value="embed v2")

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

        try:
            os.remove(f"{folder}/text/{ctx.guild.id}.csv")
        except:
            pass

        try:
            os.remove(f"{folder}/text/{ctx.guild.id}.csv")
        except:
            pass

        try:
            os.remove(f"{folder}/text/{ctx.guild.id}.csv")
        except:
            pass

        try:
            os.remove(f"{folder}/ce/{ctx.guild.id}.csv")
        except:
            pass



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

            try:
                commandMaker = CommandMaker("text", guild, self.bot)

                commandMaker.delete_command(ctx.author,command)

                await ctx.send("<:greenTick:596576670815879169> | deleted")

            except:

                try:
                    commandMaker = CommandMaker("choice", guild, self.bot)
                    commandMaker.delete_command(ctx.author, command)
                    await ctx.send("<:greenTick:596576670815879169> | deleted")
                except:
                    try:
                        commandMaker = CommandMaker("embed", guild, self.bot)

                        commandMaker.delete_command(ctx.author, command)

                        await ctx.send("<:greenTick:596576670815879169> | deleted")
                    except:

                        try:
                            commandMaker = CommandMaker("ce", guild, self.bot)

                            commandMaker.delete_command(ctx.author, command)

                            await ctx.send("<:greenTick:596576670815879169> | deleted")

                        except:

                            await ctx.message.add_reaction("❌")







        except:
            await ctx.send("command does not exist?")

    @delete.error
    async def delete_error(self,ctx,error):
        if isinstance(error, commands.CommandInvokeError):

            if str(error.original) == "You are not the owner of that command":
                await ctx.send(":x: | you don't seem to be the owner of that command")
            else:
                pass

    @commands.command()
    async def run(self, ctx, name):
        await exec(ctx=ctx, name=name, bot=self.bot)















def setup(bot):
    bot.add_cog(Utility(bot))



