import discord
from discord.ext import commands
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
import requests
import aiohttp
import operator


class Fortnite:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.data = dataIO.load_json("data/fortnite/players.json")
        self.apikey = 'QS5PLx4gAdhecXk8lsNy'

    @commands.command()
    async def fnranks(self):
        """This command gives the leaderboard of all of the fortnite players on this server's stats"""
        rankings = {}
        for discordid in self.data:
            response = requests.get('https://fortnite.y3n.co/v2/player/' + self.data[discordid], headers={'X-Key': self.apikey})
            await self.bot.say('loading player...')
            data = response.json()
            rating = self.getrating(data)

            for server in self.bot.servers:
                member = discord.utils.find(lambda m: m.id == discordid, server.members)
                if member:
                    rankings[member.name] = rating
                    break


        leaderboard = sorted(rankings.items(), key=operator.itemgetter(1))
        leaderboard.reverse()

        printstr = 'Wiff City United Fortnite Ratings\n'
        for index, tuple in enumerate(leaderboard):
            printstr += (str(index + 1) + ' - ' + str(tuple[0]) + ': ').ljust(15) + str(tuple[1]).ljust(15) + '\n'

        await self.bot.say(printstr)

    @commands.command(pass_context=True)
    async def linkfort(self, ctx, username):
        """Call this command with your username to link your discord account to your fortnite account in this server"""

        discordID = ctx.message.author.id
        try:
            data = requests.get('https://fortnite.y3n.co/v2/player/' + username, headers={'X-Key': self.apikey})
            if data.status_code != 200:
                raise Exception
        except:
            await self.bot.say('This account doesn\'t seem to exist. Did you spell your username right?')
            return

        self.data[discordID] = username
        dataIO.save_json("data/fortnite/players.json", self.data)
        await self.bot.say('Username ' + str(username) + ' successfully linked')


    def getrating(self, data):
        """This gives an adjusted rating of win rating * k/d normalized"""
        winrate = data['br']['stats']['pc']['all']['winRate']
        kd = data['br']['stats']['pc']['all']['kpd']

        return round(((winrate + kd) * 10), 2)


def setup(bot):
    bot.add_cog(Fortnite(bot))
