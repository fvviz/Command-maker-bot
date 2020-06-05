import pandas as pd
import discord
from discord.ext import commands



def make_csv(guild):
    df = pd.DataFrame(columns=['name', 'content', 'authorID'])
    df.to_csv(f"data/{guild.id}.csv",index=False)


class CommandMaker():

    def __init__(self,guild :discord.Guild,bot):
        self.guildname = guild.id

        try:
           pd.read_csv(f"data/{self.guildname}.csv")

        except:
           make_csv(guild)

        self.df =  pd.read_csv(f"data/{self.guildname}.csv")

        self.bot = bot

        commandlist = self.df.name.tolist()

        self.commandlist = commandlist

        self.commands = ""

        for command in commandlist:
            self.commands += f"`{command}"










    def save(self):
        self.df.to_csv(f"data/{self.guildname}.csv" , index=False)

    def does_command_exist(self,name):

        df = self.df

        if name in df.name.values:
            return True

        botcommands = []
        for command in self.bot.commands:
            botcommands.append(command.name)


        if name in botcommands:

            return True
        else:
            return False

    def custom_command_exists(self,name):

        df = self.df

        if name in df.name.values:
            return True

        else:
            return False

    def show_commands(self):

        df = self.df

        commandlist = df.name.tolist()

        print(commandlist)

        commands = ""

        for command in commandlist:
            commands += f"{command}\n"

        return commands




    def create_command(self,name,author:discord.Member,content):


        df = self.df

        newRow = {'name': name, 'content': content, 'authorID': author.id}
        self.df = df.append(newRow,ignore_index = True)
        self.save()


    def delete_command(self,author : discord.Member,name):

        df = self.df
        cmdRow  = df[df.name == name]
        perms = author.guild_permissions

        if cmdRow.authorID.values[0] == int(author.id):
            self.df = df[df.name != name]
            self.save()


        elif perms.administrator:
            self.df = df[df.name != name]
            self.save()


    def edit_command(self,name,author : discord.Member,content):

        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.content.values[0] = content

            df[df.name == name] = cmdRow
            self.df = df
            self.save()



        else:
            raise Exception("You are not the owner of that command")












    def run_command(self,name):



        df = self.df

        if name in df.name.values:
            commandRow = df[df.name == name]
            content = commandRow.content

            return content.values[0]
        else:

            raise Exception("command not found")

def check_existence(guild : discord.Guild):

    try:
        pd.read_csv(f"data/{guild.id}")

    except:
        return False