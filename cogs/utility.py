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


tick = "<a:green:713431758124744714>"

class Utility(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    def has_cm_perms(ctx):
        ph = PermsHandler(ctx.guild)
        return ph.has_perms(ctx.author,ctx.bot)

    @commands.group(aliases=["makecmd"])
    @commands.check(has_cm_perms)
    async def make(self, ctx):

        """
To make a command ,
use `{prefix}make <command-type><command-name>`


:pencil: **__Available Command Types__**

Click on a particular command type
to learn more about it
• [`text`](https://docs.command-maker.ml/command-types/text-commands)
• [`choice`](https://docs.command-maker.ml/command-types/choice-commands)
• [`embed`](https://docs.command-maker.ml/command-types/embed-commands)

"""
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

        """
        A text command is a command that outputs some text when called
        This command is used to make a text command.
        It takes 2 arguments

        1) name - name of the command you want to make
        2) content - the content of your command
        """
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

                    await ctx.send(f"{tick} | command **{name}** available ",delete_after = 5)
                    commandMaker.create_text_command(name, ctx.author,
                                                     await commands.clean_content().convert(ctx, content))


                    await ctx.send(content=f"{tick}  | command created ")


            else:
                await ctx.send(
                    content=f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")

    @make.command(cooldown_after_parsing = True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def choice(self, ctx, name, *, choices):
        """

        Choice commands are commands that outputs choices that are provided when the command was made, An example of a choice command would be an Magic 8Ball command

        This command takes in 3 arguments
        • name - the name of the command that you want to make
        • choices - a set of choices to pick from

        Note that **choices** have to be separated with /
        `example` - `cm-make ask yes/no`

        """
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
                    await ctx.send(f"{tick} | command **{name}** available ")

                    if "/" in choices:
                        choices = await commands.clean_content().convert(ctx, choices)
                        print(choices)
                        choicelist = choices.split("/")

                        if len(choicelist) > 1:

                            commandMaker.make_choice_command(name, ctx.author, choices)
                            await ctx.send(f"{tick} | command **{name}** created")
                        else:
                            await ctx.send(content=f":x: | bruh you can't just have one choice , try adding more")

                    else:
                        await ctx.send("Choices must be separated by / ,To learn more about choice commands head over to \nhttps://docs.command-maker.ml/command-types/choice-commands")

            else:
                        await ctx.send(f"{ctx.author.mention} bruh dat command name be af long doe , try making it shorter maybe?")


    @make.command()
    @commands.cooldown(3, 3600, BucketType.member)
    async def embed(self,ctx,name,*,code):

        """
        This command is used to make custom embed commands.

        It takes 2 arguments
        1) name - name of your command
        2) code - the json code for the embed

        In the latest update , A new system for creating embeds have been added.
        You do not have to make make them using subcommands anymore All you have to do is

        1) Head over to this [Website](https://embedbuilder.nadekobot.me/)
        2) Generate json code
        3) Copy it and then execute this command
        """

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

                        await ctx.send(f"{tick} | command **{name}** available ", delete_after=5)


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
                                await ctx.send(content=f"{tick}  | command created ")


                        except ValueError:
                            await ctx.send(f"the provided code does not seem to be valid")
                            embed = discord.Embed(color=discord.Color.dark_blue())
                            prefix = get_custom_prefix(ctx,PrefixHandler)
                            embed.title = "Making embeds"

                            embed.description = f"""
                                        In the latest update , A new system for creating embeds have been added.
                                        You do not have to make make them using subcommands anymore . All you have to do is 

                                        1) Head over to this [Website](https://embedbuilder.nadekobot.me/)
                                        2) Generate json code
                                        3) Copy it and then execute `{prefix}make embed <command-name> <code>`            
                                        """

                            embed.set_image(
                                url="https://media.discordapp.net/attachments/726816340811186227/727843773505208401/unknown.png?width=1201&height=522")
                            embed.set_thumbnail(url=self.bot.user.avatar_url)

                            await ctx.send(embed=embed)

    @make.command(cooldown_after_parsing = True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def rate(self,ctx,name,rate,*,msg = None):
        """
        A rate command outputs a random rate given a given a total
        This rate is returned in a variable **`<rate>`**

        *This command takes 3 arguments*


        [1] The **name** of the command

        [2] The **total number** to pick the rate from . If 5 is provided , Then a number between 0 and 5 maybe selected

        [3] The **Message** to send . This message needs to include the variable `<rate>` . All the other variables work here too, But this variable `<rate>` is compulsory, This is the number that will be selected from the total rate provided

        Here is an example
        `{prefix}make rate rate_me 5 I rate you <rate>/5`

        Now a random number between 0 and 5 may be selected, Lets assume its 3

        Then this outputs : `I rate you 3/10`

        """
        guild = ctx.guild

        prefix = get_custom_prefix(ctx, PrefixHandler)

        try:
            pd.read_csv(f"{folder}/text/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild.id, "text")

        commandMaker = CommandMaker('rate', guild, self.bot)

        if commandMaker.does_command_exist(name):
            await ctx.send(":x: | A command with that name already exists")

        else:

            if len(name) < 12:
                if name.startswith("@") or name.startswith("{"):
                    await ctx.send(":x: | command names cant start with `@` or `{`")
                else:

                    if msg:
                        if "<rate>" in msg:
                            print("<rate>")

                            msg = await commands.clean_content().convert(ctx,msg)

                            print(msg)

                            commandMaker.make_rate_command(name,rate,msg,ctx.author)

                    
                            await ctx.send(f"{tick} | command created")
                    else:


                        try:
                            r8 = int(rate)

                            msg = None

                            commandMaker.make_rate_command(name, rate, msg, ctx.author)
                            await ctx.send(f"{tick} | command created")

                        except:

                            await ctx.send(f"rate has to be an integer, Do {prefix}help make rate for more help")

    @make.error
    async def make_error(self, ctx, error):


        if isinstance(error,commands.CheckFailure):

            ph = PermsHandler(ctx.guild)
            role_id = ph.get_role()
            role_name = ctx.guild.get_role(role_id).name
            await ctx.send(f"{ctx.author.mention} you are missing `{role_name}` role to make commands")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} :danger:  **Missing Argument** {error.param}")


    @embed.error
    async def embed_error(self,ctx,error):

        if isinstance(error,commands.MissingRequiredArgument):
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.title = "Making embeds"

            embed.description = """
            In the latest update , A new system for creating embeds has been added.
            You do not have to make make them using subcommands anymore . All you have to do is 
            
            1) Head over to this [Website](https://embedbuilder.nadekobot.me/)
            2) Generate json code
            3) Copy it and then execute `cm-make embed <command-name> <code>`            
            """

            embed.set_image(url="https://media.discordapp.net/attachments/726816340811186227/727843773505208401/unknown.png?width=1201&height=522")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)


    @text.error
    async def text_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):



            tokenmaker = TokenMaker(ctx.author)

            await reset_timer(ctx = ctx,command_name="make text",bot=self.bot,tokenmaker=tokenmaker,error = error,rate_limit=3)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{error.param} is a required argument, Please read :arrow_heading_down: ")
            await ctx.send_help("make rate")

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
            await ctx.send(f"{error.param} is a required argument, Please read :arrow_heading_down: ")
            await ctx.send_help("make rate")


    @rate.error
    async def rate_error(self,ctx,error):

        if isinstance(error, commands.CommandOnCooldown):
            tokenmaker = TokenMaker(ctx.author)

            await reset_timer(ctx = ctx,
                              command_name="make rate",
                              bot = self.bot,
                              tokenmaker=tokenmaker,
                              error = error,
                              rate_limit=  3)

        if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"{error.param} is a required argument, Please read :arrow_heading_down: ")
                await ctx.send_help("make rate")






    @commands.group()
    #@commands.cooldown(3, 3600, BucketType.member)
    async def edit(self, ctx):

        """
To edit a command,
use `{prefix}edit <command-type> <name> <content>`

:pencil: **__Available Command Types__**
Click on a particular command type
to learn more about it
• [`text`](https://docs.command-maker.ml/command-types/text-commands#editing-text-commands)
• [`choice`](https://docs.command-maker.ml/command-types/choice-commands#making-choice-commands)
• [`embed`](https://docs.command-maker.ml/command-types/embed-commands)

        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Editing commands",
                                  color=discord.Color.dark_blue(),
                                  url = "https://docs.command-maker.ml/")

            embed.description = f"""To edit a command,
use `{prefix}edit <command-type> <name> <content>`

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
        """
        This command is used to edit text commands
        It takes 3 arguments

        1) name - the name of the command that you want to make
        2) content - the new content

        """
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
                await newmsg.edit(content=f"{tick} | **checks completed**")
                newmsg2 = await ctx.send(f"<a:loading:718075868345532466> | **editing command** `{name}`")
                await asyncio.sleep(2)
                await newmsg2.edit(
                    content=f"{tick} | **command `{name}` edited successfully**")

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

    @edit.command(name="embed", cooldown_after_parsing=True)
    @commands.cooldown(3, 3600, BucketType.member)
    async def embed_edit(self, ctx, name,*,code):
        """
        This command used to edit commands.
        It takes 2 arguments.

        1) name - the name of the command which you want to edit
        2) code - the json code of the embed

        :tools:  ***Want to generate json code for your embed ? Its easy - [Click here](https://embedbuilder.nadekobot.me/)***

        """

        guild = ctx.guild

        try:
            pd.read_csv(f"{folder}/ce/{guild.id}.csv")
        except FileNotFoundError:
            make_csv(guild=guild, type="ce")
        commandMaker = CommandMaker("ce", guild, self.bot)

        if commandMaker.custom_command_exists(name):
            await asyncio.sleep(2)

            await ctx.send(content=f"{tick} | command **{name}** exists",delete_after=2)

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
                    commandMaker.edit_ce_command(name, ctx.author, code)

                await ctx.send(
                    content=f"{tick} | **command `{name}` edited successfully**")

            except Exception as error:
                await asyncio.sleep(2)
                await ctx.send(content=f":x: | **checks failed** : `{error}`")

        elif commandMaker.does_command_exist(name):
            await asyncio.sleep(2)
            await ctx.send(content=f":x: | **Nice try , But Built-in commands cannot be edited**")

        else:
            await asyncio.sleep(2)
            await ctx.send(content=f":x: | **Command does not exist**",delete_after = 2)





    @commands.command(hidden = True)
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

        """
        Shows information about a command . This includes command type and the command author
        This command takes 1 argument and that is the name of that command

        """

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
        """
        Deletes all custom commands from a server , `Administrator` permissions are required to execute this
        """
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
        """
        This command is used to delete a custom command.
        It takes 1 argument and that is name of the command that you want to delete
        """

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

    @commands.command(hidden = True)
    async def run(self, ctx, name):
        await exec(ctx=ctx, name=name, bot=self.bot)















def setup(bot):
    bot.add_cog(Utility(bot))



