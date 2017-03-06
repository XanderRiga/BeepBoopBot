import discord
from discord.ext import commands
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
from .trainerobject import TrainerObject
import json

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
            await self.bot.say(x + ": " + self.trainercodes[x])

    @commands.command(pass_context=True)
    async def addcode(self, ctx, trainercode, description):
        """Add a code to our database of trainer codes!"""
        string = ctx.message.content.split()

        ls = " ".join(string[2:])
        newcode = TrainerObject(string[1], ls)
        self.trainercodes[string[1]] = ls
        dataIO.save_json("data/trainercodes/trainercodes.json", self.trainercodes)
        await self.bot.say("You have entered the following trainer code into the database: \n" + newcode.toString())

    @commands.command(pass_context=True)
    async def removecode(self, ctx, trainercode):
        """Remove a code from the database"""
        try:
            for x in self.trainercodes:
                if x == trainercode:
                    self.trainercodes.pop(x, None)
                    dataIO.save_json("data/trainercodes/trainercodes.json", self.trainercodes)
                    await self.bot.say("You have removed the code " + trainercode + " from the database")
                    return
            await self.bot.say("This code does not exist in the database")
        except:
            await self.bot.say("This code does not exist in the database")


def setup(bot):
    if soupAvailable:
        bot.add_cog(Trainer(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")