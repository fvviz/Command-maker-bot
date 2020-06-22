import pandas as pd
import discord
import os

def make_csv():
    df = pd.DataFrame(columns=['voterID'])
    df.to_csv(f"dblvotes/voters.csv", index=False)


def get_csv():
    try:
        pd.read_csv(f"dblvotes/voters.csv")
    except FileNotFoundError:
        make_csv()

    df = pd.read_csv(f"dblvotes/voters.csv")
    return df

class Votelister():

     def __init__(self):

         self.df = get_csv()

     def save(self):
         self.df.to_csv(f"dblvotes/voters.csv", index=False)

     def clear_votes(self):
         os.remove(f"dblvotes/voters.csv")
         make_csv()

     def has_voted(self,member : discord.Member):

         df = self.df
         ids = df.name.voterID.values

         return int(member.id) in ids

     def add_voter(self,voter : discord.Member):

         id = voter.id

         self.df.append({"voterID" : id},ignore_index=True)
         self.save()



