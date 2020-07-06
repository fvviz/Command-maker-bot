import pandas as pd
import discord
import os
import datetime

filepath = f"data/cmtokens/cmtokens.csv"

def make_csv():
    df = pd.DataFrame(columns=['memberID','timestamp'])
    df.to_csv(filepath, index=False)


def get_csv():
    try:
        pd.read_csv(filepath)
    except FileNotFoundError:
        make_csv()

    df = pd.read_csv(filepath)
    return df


class VoteHandler():

    def __init__(self, member: discord.Member):
        self.member = member


        self.df = get_csv()

        id = member.id
        ids = self.df.memberID



    def save(self):
        self.df.to_csv(filepath, index=False)

    def get_stamp(self):

        member_row = self.df[self.df.memberID == self.member.id]
        stamp = member_row.timestamp.values[0]
        return stamp

    def add_vote(self,time : datetime.datetime):

        member = self.member
        stamp = time.now()

        new_row = {"memberID": member.id,
                   "timestamp": stamp
                   }

        self.df = self.df.append(new_row,ignore_index = True)
        self.save()

    def rm_vote(self):
        member = self.member

        self.df = self.df[self.df.memberID != member.id]
        self.save()








