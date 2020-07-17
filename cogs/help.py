import discord
from discord.ext import commands
from utils.helperFuncs import *


class NewHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        ctx = self.context
        prefix = self.clean_prefix
        cog_dict = {
            "Utility": "🛠️ **Utility Commands**",
            "Meta": "📪 **Meta Commands**",
            "Configs": "⚙ **Configs**",
            "Info": "❓ **Info**"
        }

        bot = ctx.bot

        cogs = []

        cogCommands = []

        for cogname in bot.cogs:

            cog = bot.get_cog(cogname)

            visible_cmds = []

            for command in cog.get_commands():
                if not command.hidden:
                    visible_cmds.append(command.name)

            if len(visible_cmds) > 0:
                cogs.append(cogname)

        for cogname in cogs:

            cog = bot.get_cog(cogname)

            commands = cog.get_commands()
            cleanedcmds = ""

            for command in commands:
                if not command.hidden:
                    cleanedcmds += f"`{prefix}{command}` "

            cogCommands.append(cleanedcmds)

        embed = discord.Embed(
            title="Command Maker bot",
            color=discord.Color.dark_blue(),
            timestamp=ctx.message.created_at,
            url="https://docs.command-maker.ml/"
        )

        embed.set_thumbnail(url=bot.user.avatar_url)

        embed.description = f"""

<:rempleased:730393914091241532> ***Invite me to your server - [Click here](https://discord.com/oauth2/authorize?client_id=717062311755513976&scope=bot&permissions=523336)***
📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
📰 ***Check out the latest news ({await get_last_msg_date(bot)}) - [Click here]({await get_last_msg(bot)})***

*Listed below are some of the in-built commands*
📘 Do **`{prefix}help <command>`** for more help on a command
📘 Do **`{prefix}help make`** to learn about making commands 

                        """

        for cog in cogs:
            if cog in cog_dict.keys():
                embed.add_field(name=cog_dict[cog], value=cogCommands[cogs.index(cog)], inline=False)

        owner = bot.get_user(247292930346319872)
        embed.set_footer(text=f"Developer : {owner}", icon_url=owner.avatar_url)

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):

        ctx = self.context
        prefix = self.clean_prefix
        cog_dict = {
            "Utility": "🛠️ **Utility Commands**",
            "Meta": "📪 **Meta Commands**",
            "Configs": "⚙ **Configs**",
            "Info": "❓ **Info**"
        }

        bot = ctx.bot

        print(type(cog))

        visible_cmds = []

        for command in cog.get_commands():
            if not command.hidden:
                visible_cmds.append(command.name)

        cleanedcmds = ""

        for command in visible_cmds:
            cleanedcmds += f"`{prefix}{command}` "
        else:
            pass

        embed = discord.Embed(title=cog_dict[cog.qualified_name],
                              color=discord.Color.dark_blue())

        doc = cog.__doc__

        if doc is None:
            doc = "\n"

        embed.description = f"""
{doc}
{cleanedcmds}

"""
        owner = bot.get_user(247292930346319872)
        embed.set_footer(text=f"Developer : {owner}", icon_url=owner.avatar_url)

        await ctx.send(embed=embed)

    def get_command_signature(self, command):
        if not command.signature and not command.parent:
            return f"`{self.clean_prefix}{command}`"

        if command.signature and not command.parent:
            return f"`{self.clean_prefix}{command} {command.signature}`"

        if not command.signature and command.parent:
            return f"`{self.clean_prefix}{command.parent}`"

        if command.signature and command.parent:
            return f"`{self.clean_prefix}{command} {command.signature}`"

    def get_command_aliases(self, command):
        if command.aliases:
            cleaned_aliases = ""

            for aliase in command.aliases:
                cleaned_aliases += f"`{aliase}` "
        else:
            return None

    def get_command_docs(self, command):

        if command.help:
            if "{prefix}" in command.help:
                command.help = command.help.replace("{prefix}",self.clean_prefix)
            return command.help
        else:
            return None

    def get_command_help(self, command):

        aliases = self.get_command_aliases(command)
        docs = self.get_command_docs(command)
        signature = self.get_command_signature(command)

        if not aliases and not signature and not docs:
            return " "
        if aliases and signature and not docs:
            return f"""
**Usage Syntax** : {self.get_command_signature(command)}
**Aliases**: {aliases}

📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
"""
        if not aliases and signature and not docs:
            return f"""
            **Usage Syntax** : {self.get_command_signature(command)}

📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
"""
        if not aliases and signature and docs:
            return f"""
{docs}

**Usage Syntax** : {self.get_command_signature(command)}

📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
"""
        else:
            return f"""
            {docs}

           **Aliases** : {aliases}
            **Usage Syntax** : {self.get_command_signature(command)}

            📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
            🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
"""

    def get_sub_commands(self, group: commands.group):

        subcmds = group.commands
        cleaned_cmds = ""

        for subcmd in subcmds:
            cleaned_cmds += f"\n`{self.clean_prefix}{subcmd}` "

        return cleaned_cmds

    def get_group_help(self, group: commands.group):

        aliases = self.get_command_aliases(group)
        docs = self.get_command_docs(group)
        subcmds = self.get_sub_commands(group)

        if not aliases and not subcmds and not docs:
            return " "
        if aliases and subcmds and not docs:
            print(1)
            return f"""
        **Subcommands** : {subcmds}
        **Aliases**: {aliases}

        📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
        🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
        """
        if not aliases and subcmds and not docs:
            print(2)
            return f"""
                    **Subcommands** : {subcmds}

        📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
        🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
        """
        if not aliases and subcmds and docs:
            print(3)
            return f"""

        {docs}
        
        **Subcommands** : {subcmds}



        📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
        🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
        """

        if aliases and subcmds and docs:
            print(4)
            return f"""
                    {docs}

                    **Aliases** : {aliases}
                    **Subcommands** : {subcmds}

                    📝 ***Head over to the manual to see usage examples - [Click here](https://docs.command-maker.ml/)***
                    🏘️ ***Join the support server for more help - [Click here](https://discord.gg/wrMpQVA)***
                    """

    async def send_command_help(self, command: commands.Command):

        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(title=f"{command}",
                              url="https://docs.command-maker.ml/",
                              color=discord.Color.dark_blue())
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.description = self.get_command_help(command)
        await ctx.send(embed=embed)

    async def send_group_help(self, group: commands.Group):

        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(title=f"{group}",
                              url="https://docs.command-maker.ml/",
                              color=discord.Color.dark_blue())
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.description = self.get_group_help(group)
        await ctx.send(embed=embed)


class Help(commands.Cog):

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = NewHelp()
        bot.help_command.cog = self


def setup(bot):
    bot.add_cog(Help(bot))