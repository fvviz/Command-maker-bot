import pandas as pd
import random
from utils.helperFuncs import *
import json


folder = "data/commands"

def make_csv(guild,type):



    if type == "text":
        df = pd.DataFrame(columns=['name', 'content', 'authorID'])
        df.to_csv(f"{folder}/{type}/{guild}.csv", index=False)

    elif type == "choice":
        df = pd.DataFrame(columns=['name', 'choices', 'authorID'])
        df.to_csv(f"{folder}/{type}/{guild}.csv", index=False)

    elif type == "embed":
        df = pd.DataFrame(columns=['name', 'title','description','color','footer','footerurl','thumbnailurl','author_name','author_url','image_url','authorID'])
        df.to_csv(f"{folder}/{type}/{guild}.csv", index=False)

    elif type == "ce":
        df = pd.DataFrame(
            columns=['name','code','authorID'])
        df.to_csv(f"{folder}/{type}/{guild}.csv", index=False)


    else:
        raise Exception("Type has to be either text, choice or embed")

def get_csv(guild,type):

        try:
            pd.read_csv(f"{folder}/{type}/{guild}.csv")
        except:
            make_csv(guild,type)

        df = pd.read_csv(f"{folder}/{type}/{guild}.csv")
        return df






class CommandMaker():

    def __init__(self,type,guild :discord.Guild,bot):
        self.guildname = guild.id

        try:
           pd.read_csv(f"{folder}/{type}/{self.guildname}.csv")

        except FileNotFoundError:
           make_csv(self.guildname,type)
            
        self.text_df = get_csv(self.guildname,"text")
        self.choice_df = get_csv(self.guildname,"choice")
        self.embed_df = get_csv(self.guildname,"embed")
        self.ce_df = get_csv(self.guildname,"ce")

        self.text_commands = self.text_df.name.tolist()
        self.choice_commands = self.choice_df.name.tolist()
        self.embed_commands = self.embed_df.name.tolist()
        self.ce_commands = self.ce_df.name.tolist()



        self.type  = type
        self.df =  pd.read_csv(f"{folder}/{type}/{self.guildname}.csv")
        self.bot = bot



        commandlist = self.text_commands + self.choice_commands + self.embed_commands + self.ce_commands
        self.commandlist = commandlist
        self.commands = ""
        for command in commandlist:
            self.commands += f"`{command}"

    def save(self):
        type = self.type
        self.df.to_csv(f"{folder}/{type}/{self.guildname}.csv" , index=False)


    def does_command_exist(self,name):

        textdf = get_csv(self.guildname,"text")
        choicedf = get_csv(self.guildname,"choice")
        embeddf = get_csv(self.guildname,"embed")
        cedf = get_csv(self.guildname,"ce")


        botcommands = []
        for command in self.bot.commands:
            botcommands.append(command.name)

        if name in textdf.name.values:
            return True

        elif name in choicedf.name.values:
            return True

        elif name in embeddf.name.values:
            return True

        elif name in cedf.name.values:
            return True

        elif name in botcommands:
            return True
        else:
            return False


    def embed_command_exists(self,name):
        embeddf = get_csv(self.guildname, "embed")

        if name in embeddf.name.values:
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

    def create_ce_command(self,name,author:discord.Member,code):


        df = self.df
        newRow = {'name': name,
                  'code': code ,
                  'authorID' : author.id}


        self.df = df.append(newRow,ignore_index = True)
        self.save()


    def make_choice_command(self,name,author:discord.Member,choices):

        df = self.df
        choiceslist = choices.split("/")

        if len(choices) > 1:
            newRow = {'name': name, 'choices': choices, 'authorID': author.id}
            self.df = df.append(newRow, ignore_index=True)
            self.save()

        else:
            raise Exception("There can't be just one choice , Provide more ")


    def make_embed_command(self,name,author : discord.Member,description):

        df =self.df
        newRow = {'name' : name ,
                  'title' : "​",
                  'description' : description,
                  'color' : "​",
                  'footer' : "​",
                  'footerurl' : "​",
                  'thumbnailurl' : "​",
                 'author_name' : "​",
                 'author_url' : "​",
                  'image_url' : "​",
                  'authorID' : author.id}
        self.df = df.append(newRow, ignore_index=True)
        self.save()


    def modfiy_embed_color(self,author : discord.Member,name,color):

        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.color.values[0] = str(color)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")

    def add_title(self,author : discord.Member,name,title):

        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.title.values[0] = str(title)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")



    def add_thumbnail(self,author : discord.Member,name,url):

        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.thumbnailurl.values[0] = str(url)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")

    def add_author_text(self,author : discord.Member,name,authorname):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.author_name.values[0] = str(authorname)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")

    def add_author_url(self,author : discord.Member,name,url):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.author_url.values[0] = str(url)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")

    def add_footer_text(self, author: discord.Member, name, authorname):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.footer.values[0] = str(authorname)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")


    def add_footer_url(self,author : discord.Member,name,url):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.footerurl.values[0] = str(url)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")

    def add_desc(self, author: discord.Member, name, desc):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.description.values[0] = str(desc)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")


    def add_image(self, author: discord.Member, name, url):
        df = self.df
        cmdRow = df[df.name == name]

        if cmdRow.authorID.values[0] == int(author.id):
            cmdRow.image_url.values[0] = str(url)

            df[df.name == name] = cmdRow
            self.df = df
            self.save()

        else:
            raise Exception("You are not the author of that command")








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




    def run_text_command(self,name,ctx):



        df = self.df

        if name in df.name.values:
            commandRow = df[df.name == name]
            content = commandRow.content

            output = get_syntax(ctx,content.values[0])

            return output


        else:

            raise Exception("command not found")


    def run_ce_command(self,name):

        df = self.df

        if name in df.name.values:
            print("name in names")
            commandRow = df[df.name == name]
            code = commandRow.code.values[0]
            embed = exec_embed(code)
            return embed
        else:
            print("name not available")

            raise Exception("command not found")

    def get_ce_image(self,ctx,name,val):
        df = self.df
        if name in df.name.values:
            print("name in names")
            commandRow = df[df.name == name]
            code = commandRow.code.values[0]
            ec = json.loads(code)

            if val in ec.keys():
                content = get_img_syntax(ctx,ec[val])
                ec[val] = content
                return ec[val]
            else:
                pass

        else:
            print("name not available")

            raise Exception("command not found")

    def get_ce_dict(self, ctx, name,val):
        df = self.df
        if name in df.name.values:
            print("name in names")
            commandRow = df[df.name == name]
            code = commandRow.code.values[0]
            ec = json.loads(code)

            if val in ec.keys():
                content = get_img_syntax(ctx, ec[val])
                ec[val] = content
                return ec[val]
            else:
                pass
        else:
            print("name not available")
            raise Exception("command not found")






    def run_choice_command(self,name):

        df = self.df

        if name in self.df.values:
            commandRow = df[df.name == name]
            choices = commandRow.choices.values[0]

            choicelist  = choices.split("/")
            choice = random.choice(choicelist)

            return choice
        else:
            raise Exception("command not found")


    def run_embed_command(self,name):
        df = self.df

        if name in self.df.values:
            commandRow = df[df.name == name]
            title = commandRow.title.values[0]
            description = commandRow.description.values[0]
            color = commandRow.color.values[0]
            thumburl = commandRow.thumbnailurl.values[0]
            imageurl = commandRow.image_url.values[0]

            footer_text = commandRow.footer.values[0]
            footer_url = commandRow.footerurl.values[0]

            authname = " "
            authurl = " "

            authname = commandRow.author_name.iloc[0]
            authurl = commandRow.author_url.iloc[0]


            embed = discord.Embed()

            try:
                  embed = discord.Embed(color=get_color(color))
            except:
                pass


            try:
                embed.description = description
            except:
                pass

            if not title == "​":
                embed.title = title
            else:
                pass

            if not thumburl == "​":
                embed.set_thumbnail(url=thumburl)
            else:
                pass

            if not imageurl== "​":
                embed.set_image(url=imageurl)
            else:
                pass

            try:
                if not authname == " ":
                    if not authurl == " ":

                        imgtype = get_content_type(authurl)

                        try:
                            if str(imgtype).startswith("image"):
                                embed.set_author(name=authname, icon_url=authurl)
                            else:
                                pass

                        except:

                            pass
                    else:
                        pass
                else:
                    pass
            except:
                pass

            try:
                if not footer_text == " ":
                    if not footer_url == " ":

                        imgtype = get_content_type(footer_url)

                        try:
                            if str(imgtype).startswith("image"):
                                embed.set_footer(text=footer_text, icon_url=footer_url)
                            else:
                                pass
                        except:

                            embed.set_footer(text=footer_text)
                    else:
                        pass
                else:
                    pass
            except:
                pass



            return embed


        else:
            raise Exception("command not found")



def check_existence(guild : discord.Guild):

    try:
        pd.read_csv(f"data/{guild.id}")

    except:
        return False