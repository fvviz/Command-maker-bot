import pandas as pd
import discord
from discord.ext import commands
import random


def make_csv(guild,type):



    if type == "text":
        df = pd.DataFrame(columns=['name', 'content', 'authorID'])
        df.to_csv(f"data/{type}/{guild}.csv", index=False)

    elif type == "choice":
        df = pd.DataFrame(columns=['name', 'choices', 'authorID'])
        df.to_csv(f"data/{type}/{guild}.csv", index=False)

    elif type == "embed":
        pass

    else:
        raise Exception("Type has to be either text, choice or embed")

def get_csv(guild,type):

        try:
            pd.read_csv(f"data/{type}/{guild}.csv")
        except:
            make_csv(guild,type)

        df = pd.read_csv(f"data/{type}/{guild}.csv")
        return df






class CommandMaker():

    def __init__(self,type,guild :discord.Guild,bot):
        self.guildname = guild.id

        try:
           pd.read_csv(f"data/{type}/{self.guildname}.csv")

        except FileNotFoundError:
           make_csv(self.guildname,type)
            
        self.text_df = get_csv(self.guildname,"text")
        self.choice_df = get_csv(self.guildname,"choice")

        self.text_commands = self.text_df.name.tolist()
        self.choice_commands = self.choice_df.name.tolist()


        self.type  = type
        self.df =  pd.read_csv(f"data/{type}/{self.guildname}.csv")
        self.bot = bot



        commandlist = self.text_commands + self.choice_commands
        self.commandlist = commandlist
        self.commands = ""
        for command in commandlist:
            self.commands += f"`{command}"










    def save(self):
        type = self.type
        self.df.to_csv(f"data/{type}/{self.guildname}.csv" , index=False)


    def does_command_exist(self,name):

        textdf = get_csv(self.guildname,"text")
        choicedf = get_csv(self.guildname,"choice")

        botcommands = []
        for command in self.bot.commands:
            botcommands.append(command.name)

        if name in textdf.name.values:
            return True

        elif name in choicedf.name.values:
            return True

        elif name in botcommands:
            return True
        else:
            return False

    def custom_command_exists(self,name):

        df = self.df

        if name in df.name.values:
            return True

        else:
            return False


    def get_command_author_id(self,name):
        df = self.df

        if name in df.name.values:
            cmdRow = df[df.name == name]
            authorid = cmdRow.authorID.values[0]
            return authorid
        else:
            return None


    def show_commands(self):

        df = self.df

        commandlist = df.name.tolist()

        print(commandlist)

        commands = ""

        for command in commandlist:
            commands += f"{command}\n"

        return commands




    def create_text_command(self,name,author:discord.Member,content):


        df = self.df
        newRow = {'name': name, 'content': content, 'authorID': author.id}
        self.df = df.append(newRow,ignore_index = True)
        self.save()



    def make_choice_command(self,name,author:discord.Member,choices):

        df = self.df
        choiceslist = choices.split(".")

        if len(choices) > 1:
            newRow = {'name': name, 'choices': choices, 'authorID': author.id}
            self.df = df.append(newRow, ignore_index=True)
            self.save()

        else:
            raise Exception("There can't be just one choice , Provide more ")


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




    def run_text_command(self,name):



        df = self.df

        if name in df.name.values:
            commandRow = df[df.name == name]
            content = commandRow.content

            return content.values[0]
        else:

            raise Exception("command not found")


    def run_choice_command(self,name):

        df = self.df

        if name in self.df.values:
            commandRow = df[df.name == name]
            choices = commandRow.choices.values[0]

            choicelist  = choices.split(".")
            choice = random.choice(choicelist)

            return choice

        else:
            raise Exception("command not found")


def check_existence(guild : discord.Guild):

    try:
        pd.read_csv(f"data/{guild.id}")

    except:
        return False