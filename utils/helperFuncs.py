import discord
import requests


color_dict = {
    "teal" : 0x1abc9c,
    "dark teal": 0x11806a,
    "green": 0x2ecc71,
    "dark green":0x1f8b4c,
    "blue": 0x3498db,
    "dark blue": 0x9b59b6,
    "purple":0x9b59b6,
    "dark purple":0x71368a,
    "magenta": 0xe91e63,
    "dark magenta":0xad1457,

}

def does_color_exist(color):
    if color in color_dict:
        return True
    else:
        return False
def get_color(name):
    if name in color_dict:
        return color_dict[name]
    else:
        raise Exception("color not found")


def get_content_type(url):
    return requests.head(url).headers['Content-Type']