import requests
import datetime
import discord
from discord.ext import commands

color_dict = {
    "teal" : 0x1abc9c,
    "dark teal": 0x11806a,
    "green": 0x2ecc71,
    "dark green":0x1f8b4c,
    "blue": 0x3498db,
    "dark blue": 0x9b59b6,
    "purple":0x9b59b6,
    "dark purple":0x71368a,
    "magenta": 0xe91e63,
    "dark magenta":0xad1457,
}

def does_color_exist(color):
    if color in color_dict:
        return True
    else:
        return False
def get_color(name):
    if name in color_dict:
        return color_dict[name]
    else:
        raise Exception("color not found")


def get_content_type(url):
    return requests.head(url).headers['Content-Type']

def dhm(td: datetime.timedelta):
        return f"{td.seconds // 3600} hours , {(td.seconds // 60) % 60} minutes"

async def reset_timer(ctx,bot : commands.Bot,command_name,tokenmaker,error,rate_limit):
    tokens = tokenmaker.tokens

    if tokens < 1:
        await ctx.send(
            f"""

:x: | Only {rate_limit} commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**
Upvote the bot to reset the timer 

            """)
    else:
        await ctx.send(f"""

    :x: Only {rate_limit} commands can be made in an hour
    You currently have **{tokens} token(s)** remaining , do you want spend one to reset the timer? `(y/n)`
    *You can earn more tokens by upvoting me* use **cm-vote**
                    """)

        def check(message):

            if message.content in "yn":
                if message.channel == ctx.channel:
                    if message.author == ctx.author:
                        return True

                    else:
                        return False

                else:
                    return False
            else:
                return False

        input = await bot.wait_for("message", check=check, timeout=30)

        if input.content == "y":
            bot.get_command(command_name).reset_cooldown(ctx)
            await input.add_reaction("<:greenTick:596576670815879169>")

        else:

            await input.add_reaction("❌")

async def guildinfo(guild,channel):

    def get_tier(guild: discord.Guild):
        if guild.premium_tier == 0:
            return f"🔷 **Level 0** ({guild.premium_subscription_count} boosts)"
        if guild.premium_tier == 1:
            return f"🔷 **Level 1** ({guild.premium_subscription_count} boosts)"
        if guild.premium_tier == 2:
            return f"🔷 **Level 2** ({guild.premium_subscription_count} boosts)"
        if guild.premium_tier == 3:
            return f"🔷 **Level 3** ({guild.premium_subscription_count} boosts)"

    embed = discord.Embed(title=f"{guild.name} ", description=guild.description,
                          color=discord.Color.dark_blue())
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="**Region :round_pushpin: **", value=f"{str(guild.region)}", inline=False)
    embed.add_field(name="**Owner :crown: **", value=guild.owner.mention, inline=False)
    embed.add_field(name="**Created at :clock7: ** ", value=f"{str(guild.created_at)[:10]}",
                    inline=False)
    embed.add_field(name="**Member Count**", value=f"{guild.member_count}", inline=False)
    embed.add_field(name="**Server Boost level**", value=get_tier(guild), inline=False)
    await channel.send(embed=embed)