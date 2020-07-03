from typing import Union

import discord
import pandas as pd

pre_folder = "data/prefixes"

def make_csv():
    df = pd.DataFrame(columns=['guildID', 'prefix', 'authorID'])
    df.to_csv(f"{pre_folder}s/prefixes.csv", index=False)


def get_csv():
    try:
        pd.read_csv(f"{pre_folder}/prefixes.csv")
    except FileNotFoundError:
        make_csv()

    df = pd.read_csv(f"{pre_folder}/prefixes.csv")
    return df


class PrefixHandler:
    df = get_csv()

    @classmethod
    def save(cls):
        cls.df.to_csv(f"{pre_folder}/prefixes.csv", index=False)

    @classmethod
    def add_prefix(cls, author: discord.Member, guild_id: int, prefix: str):
        if guild_id not in cls.df.guildID.values:

            print("if not self.guildID in df.guildID.values:")
            new_row = {
                "guildID": guild_id,
                "prefix": prefix,
                "authorID": author.id
            }

            # TODO why overwrite it?
            cls.df = cls.df.append(new_row, ignore_index=True)
            print("appended")
            cls.save()
        else:
            print("else")
            guild_row = cls.df[cls.df.guildID == guild_id]
            guild_row.prefix.values[0] = prefix
            cls.df[cls.df.guildID == guild_id] = guild_row
            cls.save()

    @classmethod
    def remove_prefix(cls,guild_id : int):
        if guild_id not in cls.df.guildID.values:
            pass
        else:

            cls.df = cls.df[cls.df.guildID != guild_id]
            cls.save()



    @classmethod
    def get_prefix(cls, guild_id: int) -> Union[str, None]:
        prefix = None

        try:
            guild_row = cls.df[cls.df.guildID == guild_id]
            prefix = guild_row.prefix.values[0]
        except:
            pass

        return prefix

    @classmethod
    def has_custom_prefix(cls, guild_id: int) -> bool:
        return guild_id in cls.df.guildID.values
