import discord
from discord.ext import commands
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import aiohttp

class Trainer:
    """Cog for Trainer Codes"""

    def __init__(self, bot):
        self.bot = bot
        self.countComs = dataIO.load_json("data/countcoms/countcoms.json")




def setup(bot):
	if soupAvailable:
		bot.add_cog(Mycog(bot))
	else:
		raise RuntimeError("You need to run `pip3 install beautifulsoup4`")