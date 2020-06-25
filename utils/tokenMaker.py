import pandas as pd
import discord
import os

filepath = f"cmtokens/cmtokens.csv"

def make_csv():
    df = pd.DataFrame(columns=['memberID','tokens'])
    df.to_csv(filepath, index=False)


def get_csv():
    try:
        pd.read_csv(filepath)
    except FileNotFoundError:
        make_csv()

    df = pd.read_csv(filepath)
    return df

class TokenMaker():

     def __init__(self,member : discord.Member):
         self.member = member

         self.df = get_csv()

         id = member.id
         ids = self.df.memberID

         tokens = 0


         if not id in ids.values:
             new_row = {"memberID": id,
                        "tokens": 0
                        }
             self.df.append(new_row, ignore_index=True)
             self.save()
             tokens = 0
         else:
             member_row = self.df[self.df.memberID == int(id)]
             tokens = member_row.tokens.values[0]

         self.tokens = tokens




     def save(self):
         self.df.to_csv(filepath, index=False)

     def clear_votes(self):
         os.remove(filepath)
         make_csv()


     def add_token(self):

         member = self.member

         id = member.id
         ids = self.df.memberID

         if not id in ids.values:
             new_row = {"memberID": id,
                        "tokens": 1
                        }
             self.df.append(new_row,ignore_index=True)
             self.save()
         else:
             member_row = self.df[self.df.memberID == int(id)]
             member_row.tokens.values[0] += 1

             self.df[self.df.memberID == int(id)] = member_row
             self.save()






















