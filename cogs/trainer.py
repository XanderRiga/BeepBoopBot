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
        self.trainercodes = dataIO.load_json("data/trainercodes/trainercodes.json")

    @commands.command()
    async def allcodes(self):
        for x in self.trainercodes:
            await self.bot.say(x.toString)

    @commands.command(pass_context=True)
    async def addcode(self, ctx, trainercode, description):
        string = ctx.message.content.split()
        
        newcode = TrainerObject(string[0], ctx.message.author.id, string[1:])


def setup(bot):
	if soupAvailable:
		bot.add_cog(Mycog(bot))
	else:
		raise RuntimeError("You need to run `pip3 install beautifulsoup4`")



class TrainerObject:
   'Object to hold trainer codes'

   def __init__(self, trainercode, author, description):
      self.trainercode = trainercode
      self.author = author
      self.description = description

    def toString():
        string = "Trainer Code: " + self.trainercode + "\nAuthor: " + self.author + "\nDescription: " + self.description
        return string