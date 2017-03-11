import discord
from discord.ext import commands
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
from .trainerobject import TrainerObject
import json
import aiohttp

class playersonline:
    """Cog for showing players online and what they are playing"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whosonline(self):
        server = discord.utils.find(lambda m: m.id == '174382936877957120', self.bot.servers)
        memberList = server.members
        membersGaming = []
        for x in memberList:
            if x.game is not None:
                membersGaming.append(x)

        gamesBeingPlayed = {}
        if len(membersGaming) == 0:
            await self.bot.say("No one is gaming right now")
            return
        else:
            for x in membersGaming:
                if x.game.name in gamesBeingPlayed:
                    gamesBeingPlayed[x.game.name] += 1
                    pass
                else:
                    gamesBeingPlayed[x.game.name] = 1

        for x in gamesBeingPlayed:
            await self.bot.say(str(gamesBeingPlayed[x]) + " player(s) playing " + x)



def setup(bot):
    bot.add_cog(playersonline(bot))