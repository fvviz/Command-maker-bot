from typing import Union
import discord
import pandas as pd

pre_folder = "data/perms"

def make_csv():
    df = pd.DataFrame(columns=['guildID', 'roleID', 'authorID'])
    df.to_csv(f"{pre_folder}/perms.csv", index=False)


def get_csv():
    try:
        pd.read_csv(f"{pre_folder}/perms.csv")
    except FileNotFoundError:
        make_csv()

    df = pd.read_csv(f"{pre_folder}/perms.csv")
    return df


class PermsHandler():

    def __init__(self,guild:discord.Guild):

         self.df = get_csv()
         self.guild = guild

    def save(self):
        self.df.to_csv(f"{pre_folder}/perms.csv", index=False)

    def add_role(self,role: discord.Role,author : discord.Member):

        guild_id = self.guild.id
        role_id = role.id
        if guild_id not in self.df.guildID.values:

            print("if not self.guildID in df.guildID.values:")
            new_row = {
                "guildID": guild_id,
                "roleID": role_id,
                "authorID": author.id
            }

            self.df = self.df.append(new_row, ignore_index=True)

            self.save()
        else:
            guild_row = self.df[self.df.guildID == guild_id]
            guild_row.roleID.values[0] = role_id
            self.df[self.df.guildID == guild_id] = guild_row
            self.save()

    def remove_role_perms(self):

        guild_id = self.guild.id


        if guild_id not in self.df.guildID.values:
            pass

        else:
            print(self.df[self.df.guildID == guild_id])
            self.df = self.df[self.df.guildID != guild_id]
            self.save()


    def get_role(self) -> Union[int, None]:

        guild_id = self.guild.id
        role_id = None

        try:
            guild_row = self.df[self.df.guildID == guild_id]
            role_id = guild_row.roleID.values[0]
            print(role_id)
        except:
            pass

        return role_id

    def has_perms_role(self) -> bool:
        guild_id = self.guild.id
        return guild_id in self.df.guildID.values

    def has_perms(self,member : discord.Member,bot) -> bool:


        if self.has_perms_role():
            guild_id = self.guild.id
            guild = bot.get_guild(guild_id)
            perms_role = guild.get_role(self.get_role())

            return perms_role in member.roles
        else:
            return True






