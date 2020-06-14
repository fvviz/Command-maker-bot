import discord
from discord.ext import commands
from utils.commandMaker import CommandMaker
import os
from setup import token
from utils.runner import run

prefix = "cm-" \
         ""
bot = commands.Bot(command_prefix=prefix)

game = discord.Game(name=f'cm-help')

@bot.event
async def on_ready():
    print('ready')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)

def launchBot(bot : commands.bot):
    bot.load_extension("cogs.utility")
    bot.remove_command("help")
    bot.load_extension("cogs.help")
    bot.load_extension("cogs.owner")
    bot.run(token)

@bot.event
async def on_guild_join(guild : discord.Guild):

    owner = bot.get_user(247292930346319872)
    ritsu = bot.get_user(717062311755513976)
    logchannel = bot.get_channel(712640308319617034)

    embed = discord.Embed(title = "Greetings",description=f"""
**__Command maker bot__**

[`Invite to your server`](https://discord.com/oauth2/authorize?client_id=717062311755513976&scope=bot&permissions=523336)

**Command maker** is a bot with which you can make your own commands. Yes , **your own commands**  
 
**:pencil: __Usage__**
To make your own commands, 
Use command `{prefix}make <command-type> <command-name-here> <content>`

**Example** : `{prefix}make text ji hi`
This should make a command called 'hi'
now you can use `{prefix}hi` anytime and the bot will respond `hi`



                        """, color = discord.Color.dark_blue())
    embed.add_field(name=f"General information",value="**► __Bot Id__**: 717062311755513976 \n**► __Developer__** : **fwiz#6999** \n**► __Prefix__** : {prefix} ")
    embed.set_thumbnail(url = ritsu.avatar_url)

    try:
        await guild.system_channel.send(embed = embed)
    except:
        pass

    await logchannel.send(f"<a:sufisheep:718395610549452901> The bot has been added to **{guild.name}** , We've reached our **{len(bot.guilds)}th** server! <a:sufisheep:718395610549452901>")


@bot.event
async def on_command_error(ctx,error):



    if isinstance(error,commands.CommandNotFound):

        command = ctx.invoked_with

        await run(ctx = ctx,name=command,bot=bot)


    else:
        pass



launchBot(bot)
