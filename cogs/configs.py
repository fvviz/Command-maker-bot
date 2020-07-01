from discord.ext import commands
from utils.permsHandler import PermsHandler
import discord
from discord.ext.commands.cooldowns import BucketType
from utils.prefixMaker import PrefixHandler
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

    @commands.command(name="remove perms")
    @commands.check(has_perms)
    async def remove_perms(self, ctx):
        ph = PermsHandler(ctx.guild)
        ph.remove_role_perms()
        await ctx.send(f"{tick} removed")

    @commands.command()
    @commands.check(has_perms)
    async def set_perms(self, ctx, *, role: discord.Role):
        ph = PermsHandler(ctx.guild)

        ph.add_role(role, ctx.author)

        await ctx.send(f"Permissions have been set. Only members with `{role.name}` can make commands now")

    @set_perms.error
    async def set_perms_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} tutorial how to download free ca")

    @commands.command(cooldown_after_parsing=True)
    @commands.check(has_perms)
    @commands.cooldown(3, 86400, BucketType.guild)
    async def prefix(self, ctx, new_prefix):
        PrefixHandler.add_prefix(author=ctx.author, guild_id=ctx.guild.id, prefix=new_prefix)
        await ctx.send(
            f"<:greenTick:596576670815879169>  | the prefix for **{ctx.guild.name}** has been to set to {new_prefix}")

    @prefix.error
    async def change_prefix_error(self, ctx, error):

        if isinstance(error, commands.CheckFailure):
            await ctx.send("you require `administrator` permissions to execute that command")

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f":x: | Only 3 commands can be edited in an hour. **Try again in {dhm(error.retry_after)}**")

def setup(bot):
    bot.add_cog(Configs(bot))