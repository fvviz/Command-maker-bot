from discord.ext import commands
from utils.permsHandler import PermsHandler
import discord
from discord.ext.commands.cooldowns import BucketType
from utils.prefixMaker import PrefixHandler
from utils.helperFuncs import *
tick = "<:greenTick:596576670815879169>"



class Configs(commands.Cog):

    def __init__(self,bot):

        self.bot = bot


    def has_cm_perms(ctx):
        ph = PermsHandler(ctx.guild)
        return ph.has_perms(ctx.author,ctx.bot)

    async def has_perms(ctx):

        if ctx.author.id == 247292930346319872:
            return True
        elif ctx.author.guild_permissions.administrator:
            return True

        else:
            return False

    @commands.group(aliases= ["perms"])
    async def permissions(self,ctx):
        """
        This command is used to control who can make commands . This works by
        only allowing members with a specific role to make commands. More information
        can be found in the manual (link below) . But to simply

        Do `cm-perms set <some-role>` to set permissions ( cm- is the universal prefix , if you
        have a custom prefix set up , that will work too)

        You will require administrator permissions to set permissions

        All the subcommands are mentioned below , Use the help command on the
        subcommands to learn more . (Better way would be to just read the manual)

        """

        prefix = get_custom_prefix(ctx,PrefixHandler)


        if ctx.invoked_subcommand is None:

            embed = discord.Embed(color=discord.Color.dark_blue(),
                                  title = "Want to control who can make commands?",
                                  url = "https://docs.command-maker.ml/configurations/permissions")



            embed.description = f"""
            In the latest update , You can control who can make commands . 
            This can be done by granting the ability to make commands only to 
            members with a certain role
            
            This can be done by invoking the `permissions set` command
            
            `{prefix}permissions set <role>`
            
            `<role>` can be mention/id or even a name of that role
            
        

            """
            embed.set_thumbnail(url=self.bot.user.avatar_url)

            await ctx.send(embed=embed)

    @permissions.command(name="remove")
    @commands.check(has_perms)
    async def remove(self, ctx):
        ph = PermsHandler(ctx.guild)
        ph.remove_role_perms()
        await ctx.send(f"{tick} removed")

    @permissions.command(name="set",aliases = ["set_perms"])
    @commands.check(has_perms)
    async def set(self, ctx, *, role: discord.Role):
        ph = PermsHandler(ctx.guild)

        ph.add_role(role, ctx.author)

        await ctx.send(f"Permissions have been set. Only members with `{role.name}` can make commands now")

    @set.error
    async def set_perms_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} ***Administrator** permissions are required to invoke that commmand")
        if isinstance(error,commands.BadArgument):
            await ctx.send(f"That role does not seem to exist . Please specify a valid role")
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("you require `administrator` permissions to execute that command")


    @commands.group(aliases = ["pre"])
    async def prefix(self,ctx):

        if ctx.invoked_subcommand is None:
            embed= discord.Embed(color = discord.Color.dark_blue(),
                                 title = "Want to set a custom prefix for your server? Click here to learn more",
                                 url="https://docs.command-maker.ml/configurations/permissions")

            embed.set_thumbnail(url=self.bot.user.avatar_url)

            prefix = get_custom_prefix(ctx,PrefixHandler)
            embed.description =f"""
            You can do by invoking
            `{prefix}prefix set <prefix>`
            `{prefix}prefix remove`
            """
            embed.set_footer(icon_url=ctx.guild.icon_url,text=f"current prefix is {prefix}")
            await ctx.send(embed=embed)

    @prefix.command(name = "set",cooldown_after_parsing=True)
    @commands.check(has_perms)
    @commands.cooldown(3, 86400, BucketType.guild)
    async def set_(self, ctx, new_prefix):
        PrefixHandler.add_prefix(author=ctx.author, guild_id=ctx.guild.id, prefix=new_prefix)
        await ctx.send(
            f"<:greenTick:596576670815879169>  | the prefix for **{ctx.guild.name}** has been to set to {new_prefix}")

    @set_.error
    async def set_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, commands.CheckFailure):
            await ctx.send("you require `administrator` permissions to execute that command")

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 prefixes can be set in a day. **Try again in {convert(error.retry_after)}**")

    @prefix.command(name="remove", cooldown_after_parsing=True)
    @commands.check(has_perms)
    async def remove_(self, ctx):
        PrefixHandler.remove_prefix(guild_id=ctx.guild.id)
        await ctx.send(
            f"<:greenTick:596576670815879169>  | the prefix for **{ctx.guild.name}** has been removed")


def setup(bot):
    bot.add_cog(Configs(bot))