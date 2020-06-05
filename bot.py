import discord
from discord.ext import commands
from utils.commandMaker import CommandMaker
import os
from setup import token

prefix = "cm/"
bot = commands.Bot(command_prefix=prefix)

game = discord.Game(name=f'{prefix}help')

@bot.event
async def on_ready():
    print('ready')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)

def launchBot(bot : commands.bot):
    bot.load_extension("cogs.utility")
    bot.remove_command("help")
    bot.load_extension("cogs.help")
    bot.run(token)


@bot.event
async def on_command_error(ctx,error):

    #if isinstance(error,commands.MissingRequiredArgument):
        #await ctx.send(f"❌| **{error}** \n__for more help on that command,use__ **rt help {ctx.command.name}**")

    #elif isinstance(error,commands.BotMissingPermissions):
        #await ctx.send("❌| **I'm missing permissions to execute that command**")

    if isinstance(error,commands.CommandNotFound):

        try:
            commandMaker = CommandMaker(ctx.guild,bot)
            print(ctx.message.content)

            output = commandMaker.run_command(name=ctx.message.content[len(prefix):])
            await ctx.send(output)

        except:

            await ctx.send(f"❌| **command does not exist**")



    else:
        await ctx.send(f"❌|{error}")
        


launchBot(bot)

