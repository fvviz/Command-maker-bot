import requests
import datetime
import discord
from discord.ext import commands
import json
import codecs
import os
import pathlib
from discord import UserFlags , Status


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

badge_dict = {

    UserFlags.staff : "<:staff:730489979058257951>",
    UserFlags.partner : "<:DiscordPartner:710860869252415630>",
    UserFlags.hypesquad : "<:hypesquad_events:585765895939424258>",
    UserFlags.bug_hunter : "<:bughunter:585765206769139723>",
    UserFlags.hypesquad_bravery : "<:bravery:710518487390486549>",
    UserFlags.hypesquad_brilliance :"<:BrillianceLogo:710518070640378021>",
    UserFlags.hypesquad_balance: "<:hsBalance:710512831463686235>",
    UserFlags.early_supporter : "<:earlysupporter:710859759938568212>",
    UserFlags.bug_hunter_level_2 : "<:bug2:710864460612632596>",
    UserFlags.verified_bot : "<:verified1:730739562703224863><:verified2:730739583934791721>",
    UserFlags.verified_bot_developer : "<:dev:710864395588206612>",
}

stat_dict = {
    Status.offline : "<:offline2:464520569929334784>",
    Status.online : "<:online2:464520569975603200>",
    Status.dnd : "<:dnd2:464520569560498197>",
    Status.idle : "🌜"

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

def get_status(member):

    if member.status in stat_dict.keys():
        return stat_dict[member.status]


def get_badges(member):

    badges = ""

    flags  = member.public_flags.all()

    for flag in flags:
        print(flag)
        if flag in badge_dict.keys():
            badges += badge_dict[flag]

    if member.is_avatar_animated:
        badges += "<:nitro:710866062924709938>"
    return badges






def format_date(join_date: datetime.datetime):
    today = datetime.date.today()
    days = join_date.date() - today
    year = int(days.days / 365)

    if year == 0:
        return f"{join_date.day} {join_date.strftime('%B')},{join_date.year}"

    return f"{join_date.day} {join_date.strftime('%B')},{join_date.year}"

def get_syntax(ctx,content):

    syntax_dict = {

        "<author>" : ctx.author,
        "<author-name>" : ctx.author.name,
        "<author-id>" : ctx.author.id,
        "<author-nick>" : ctx.author.nick,
        "<author-mention>" : ctx.author.mention,
        "<author-created-at>" : format_date(ctx.author.created_at),
        "<author-joined-at>" : format_date(ctx.author.joined_at),
        "<member-count>"  : ctx.guild.member_count,
        "<author-pfp>" : ctx.author.avatar_url,
        "<author-av>" : ctx.author.avatar_url,
        "<author-badges>" : get_badges(ctx.author),
        "<author-status>" : get_status(ctx.author),
        "<guild-icon>" : ctx.guild.icon_url,
        "<guild-banner>" : ctx.guild.banner_url,
        "<guild-splash-url>" : ctx.guild.splash_url,
        "<guild>" : ctx.guild.name,
        "<guild-id>" : ctx.guild.id,
        "<guild-created-at>" : ctx.guild.created_at,
        "<guild-owner>" : ctx.guild.owner,
        "<guild-boost-level>" : ctx.guild.premium_tier,
        "<guild-boosts>" : ctx.guild.premium_subscription_count,
        "<guild-boosters>" : len(ctx.guild.premium_subscribers),
        "<guild-channels>" : len(ctx.guild.channels),
        "<guild-voice-channels>" : len(ctx.guild.voice_channels),
        "<guild-text-channels>" : len(ctx.guild.text_channels),
        "<guild-emoji-limit>" : ctx.guild.emoji_limit,
        "<guild-roles>" : len(ctx.guild.roles),

    }


    for i in list(syntax_dict.keys()):
            if i in content:
                content=content.replace(i,str(syntax_dict[i]))
            else:
                pass

    return content

def get_custom_prefix(ctx,PrefixHandler):
    cust_prefix = None

    if PrefixHandler.has_custom_prefix(ctx.guild.id):
        cust_prefix = PrefixHandler.get_prefix(ctx.guild.id)

    if cust_prefix is None:

        cust_prefix = "cm-"

    return cust_prefix



async def get_last_msg_date(bot):

    channel = bot.get_channel(717638909281959966)
    last = await channel.history(limit = 1).flatten()
    return format_date(last[0].created_at)


async def get_last_msg(bot):

    channel = bot.get_channel(717638909281959966)
    last = await channel.history(limit = 1).flatten()
    return last[0].jump_url










def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60

    return f"{int(hour)} hour(s) , {int(minutes)} minute(s)"

def linecount():
    total = 0
    file_amount = 0

    for path, subdirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.py'):
                file_amount += 1
                with codecs.open('./' + str(pathlib.PurePath(path, name)), 'r', 'utf-8') as f:
                    for i, l in enumerate(f):
                        if l.strip().startswith('#') or len(l.strip()) is 0:  # skip commented lines.
                            pass
                        else:
                            total += 1

    return total,file_amount

def get_img_syntax(ctx,content):

    syntax_dict = {
        "<author-pfp>" : ctx.author.avatar_url,
        "<author-av>" : ctx.author.avatar_url,
        "<guild-icon>" : ctx.guild.icon_url
    }


    for i in list(syntax_dict.keys()):
            if i in content:
                content=content.replace(i,str(syntax_dict[i]))

                print(f"{i} --> {syntax_dict[i]}")
            else:
                pass

    return content

def in_img_syntax(ctx,content):
    syntax_dict = {
        "<author-pfp>": ctx.author.avatar_url,
        "<author-av>": ctx.author.avatar_url,
        "<guild-icon>": ctx.guild.icon_url
    }

    return content in syntax_dict.keys()


def bytes_format(bytes):
    kb =  bytes/1000
    mb = 0
    gb = 0
    val = f"{kb} KB"


    if kb > 1000:
        mb = round(kb/1000)
        val = f"{mb} MB"

    if mb > 1000:
        gb = mb/1000
        val = f"{gb} GB"

    return val





def get_content_type(url):
    return requests.head(url).headers['Content-Type']


def is_image(url):

    type = get_content_type(url)

    if str(type).startswith("image"):
        return True
    else:
        return False


def format_rr_message(ctx,ph):

    if ph.has_perms_role():
        role_id = ph.get_role()

        print("role:",role_id)
        role = ctx.guild.get_role(role_id)

        content = f"*`only members with {role.name} role will be able to make commands`*"

        return content

    else:
        return ""


def bool_to_em(val:bool):
    enabled = "<:enable:727107200958464060>"
    disabled = "<:disable:727107239957102643>"

    if val:
        return enabled
    else:
        return disabled


def exec_embed(code):
        print(code)

        try:
            embed_code = json.loads(code,strict = False)

            removals = ["image","thumbnail","author","footer"]

            for i in removals:
                if i in embed_code.keys():
                    embed_code.pop(i)

            embed = discord.Embed.from_dict(embed_code)
            return embed

        except ValueError:
            print("error")


def check_embed(ec):

    check_dict =    {
        "author_icon" : True,
        "image" : True,
        "footer_icon" : True,
        "thumbnail" : True
    }

    syntaxes = [ "<author-pfp>","<author-av>","<guild-icon>"]

    if "author" in ec.keys():
        ad = ec["author"]

        if "icon_url" in ad.keys():

            try:
                if is_image(ad["icon_url"]):
                    pass

                elif ad["icon_url"] in syntaxes:
                    pass

                else:
                    check_dict["author_icon"] = False

            except requests.exceptions.MissingSchema:

                if ad["icon_url"] in syntaxes:
                    pass

                else:
                    check_dict["author_icon"] = False

        else:
            pass

        if "image" in ec.keys():
            try:

                if is_image(ec["image"]):
                    pass
                elif ec["image"] in syntaxes:
                    pass
                else:
                    check_dict["image"] = False
            except:
                if ec["image"] in syntaxes:
                    pass

                else:
                    check_dict["image"] = False

    if "thumbnail" in ec.keys():

        try:
            if is_image(ec["thumbnail"]):
                pass

            elif ec["thumbnail"] in syntaxes:
                pass
            else:
                check_dict["thumbnail"] = False
        except requests.exceptions.MissingSchema:

            if ec["thumbnail"] in syntaxes:
                pass
            else:
                 check_dict["thumbnail"] = False

    if "footer" in ec.keys():

        ad = ec["footer"]

        if "icon_url" in ad.keys():

            try:
                if is_image(ad["icon_url"]):
                    pass
                elif ad["icon_url"] in syntaxes:
                    pass
                else:
                    check_dict["footer_icon"] = False

            except requests.exceptions.MissingSchema:

                if ad["icon_url"] in syntaxes:
                    pass

                else:
                    check_dict["footer_icon"] = False
        else:
            pass

    return check_dict




def process_embed(ctx,embed : discord.Embed,auth_dict = None,footer_dict = None):

    new_embed = embed



    try:
       new_embed.title = get_syntax(ctx,embed.title)

    except:
        pass
    try:
       new_embed.description = get_syntax(ctx,embed.description)
    except:
        pass

    if auth_dict is not None:

        if "name" in auth_dict.keys():
            auth_name = get_syntax(ctx,auth_dict["name"])

            new_embed.set_author(name=auth_name)

        if "icon_url" in auth_dict.keys():
            auth_name = get_syntax(ctx, auth_dict["name"])
            auth_icon_url = get_img_syntax(ctx, auth_dict["icon_url"])

            embed.set_author(name=auth_name, icon_url=auth_icon_url)

        if "url" in auth_dict.keys():
            auth_name = get_syntax(ctx, auth_dict["name"])
            auth_icon_url = get_img_syntax(ctx, auth_dict["icon_url"])
            auth_url = get_syntax(ctx, auth_dict["url"])

            new_embed.set_author(name=auth_name,
                              icon_url=auth_icon_url,
                              url=auth_url)

        else:
            pass

    if footer_dict is not None:

        if "text" in footer_dict.keys():
            foot_text = get_syntax(ctx,footer_dict["text"])

            new_embed.set_footer(text=foot_text)

        if "icon_url" in footer_dict.keys():
            foot_text = get_syntax(ctx,footer_dict["text"])
            foot_icon_url = get_img_syntax(ctx, footer_dict["icon_url"])

            new_embed.set_footer(text=foot_text, icon_url=foot_icon_url)
        else:
            pass


    if len(embed.fields) > 0:

        index = 0
        field_count = len(embed.fields)

        for count in range(field_count):
            og_field = embed.fields[index]
            val = og_field.value
            name = og_field.name

            embed.set_field_at(index,value=get_syntax(ctx,val),name=name)
            index += 1



    return new_embed





def dhm(td: datetime.timedelta):
        return f"{td.seconds // 3600} hours , {(td.seconds // 60) % 60} minutes"

async def reset_timer(ctx,bot : commands.Bot,command_name,tokenmaker,error,rate_limit):
    tokens = tokenmaker.tokens

    print(tokens)

    if tokens < 1:
        await ctx.send(
            f"""

:x: | Only {rate_limit} commands can be made in an hour. **Try again in {str(datetime.timedelta(seconds=error.retry_after))[2:4]} minutes**
Upvote the bot to reset the timer ; https://top.gg/bot/717062311755513976/vote
            """)
    else:
        await ctx.send(f"""

    :x: Only {rate_limit} commands can be made in an hour
    You currently have **{int(tokens)} token(s)** remaining , do you want spend one to reset the timer? `(y/n)`
    *You can earn more tokens by upvoting me (link below)
    https://top.gg/bot/717062311755513976/vote
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
            await input.add_reaction("<a:green:713431758124744714>")
            tokenmaker.rm_token()

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