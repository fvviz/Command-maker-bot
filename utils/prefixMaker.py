import pandas as pd
import discord

def make_csv():

        df = pd.DataFrame(columns=['guildID', 'prefix', 'authorID'])
        df.to_csv(f"prefixes/prefixes.csv", index=False)

def get_csv():

        try:
            pd.read_csv(f"prefixes/prefixes.csv")
        except FileNotFoundError:
            make_csv()

        df = pd.read_csv(f"prefixes/prefixes.csv")
        return df

class PrefixMaker():

    def __init__(self,guild):

        self.guildID = guild.id
        self.df = get_csv()

    def save(self):
        self.df.to_csv(f"prefixes/prefixes.csv" , index=False)

    def add_prefix(self,author: discord.Member,prefix):

        df = self.df

        if not self.guildID in df.guildID.values:

            print("if not self.guildID in df.guildID.values:")
            new_row = {     "guildID" : self.guildID,
                            "prefix" : prefix,
                            "authorID" : author.id}

            self.df = self.df.append(new_row,ignore_index=True)
            print("appended")
            self.save()
        else:
            print("else")
            guild_row = df[df.guildID == int(self.guildID)]

            guild_row.prefix.values[0] = prefix

            self.df[self.df.guildID == int(self.guildID)] = guild_row
            self.save()




    def get_prefix(self):

        prefix = None
        df = self.df


        try:
                guild_row = df[df.guildID == int(self.guildID)]
                print(guild_row)
                prefix = guild_row.prefix.values[0]
        except:
            pass

        if prefix is not None:
            return prefix
        else:
            return None

    def has_custom_prefix(self):

        df = self.df

        return self.guildID in df.guildID.values


















