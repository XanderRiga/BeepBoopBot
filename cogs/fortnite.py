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
        """This gives the rank leaderboard with more detail than regular fnranks"""

        self.data = dataIO.load_json("data/fortnite/players.json")
        rankings = {}
        winrates = {}
        kds = {}
        failed = 0
        for discordid in self.data:
            try:
                response = requests.get('https://fortnite.y3n.co/v2/player/' + self.data[discordid], headers={'X-Key': self.apikey})
                if response.status_code != 200:
                    raise Exception
            except:
                failed += 1
                continue

            try:
                data = response.json()
                rating = self.getrating(data)
                winrate = self.getwinrate(data)
                kd = self.getkd(data)
            except:
                failed += 1
                continue

            for server in self.bot.servers:
                member = discord.utils.find(lambda m: m.id == discordid, server.members)
                if member:
                    rankings[member.name] = rating
                    winrates[member.name] = winrate
                    kds[member.name] = kd
                    break

        if not rankings:
            await self.bot.say('Uh oh! Looks like the API for player data might be down, try again later')
            return

        leaderboard = sorted(rankings.items(), key=operator.itemgetter(1))
        leaderboard.reverse()

        printstr = '```Wiff City United Detailed Fortnite Ratings\n\n'
        printstr += 'Rank'.ljust(7) + 'Name'.ljust(15) + 'Rating'.ljust(12) + 'Winrate'.ljust(12) +'K/D'.ljust(12) + '\n'
        printstr += '---------------------------------------------------\n'
        for index, tuple in enumerate(leaderboard):
            name = tuple[0]
            rating = tuple[1]
            wr = winrates[name]
            kd = kds[name]
            printstr += str(index + 1).ljust(7) + str(name).ljust(15) + str(rating).ljust(12) + str(wr).ljust(12) + str(kd).ljust(12) +'\n'

        printstr += '```'
        await self.bot.say(printstr)
        if failed > 0:
            await self.bot.say(str(failed) + ' players data could not be found. If your name is not on the list then you may have spelled it wrong, try using !fnlink to reset your name')


    @commands.command(pass_context=True)
    async def fnremove(self, ctx):
        """This removes you from the fnranks leaderboard"""

        self.data = dataIO.load_json("data/fortnite/players.json")
        discordid = ctx.message.author.id
        self.data.pop(discordid, None)

        dataIO.save_json("data/fortnite/players.json", self.data)
        await self.bot.say('Successfully removed you from the rankings. Use !linkfort to add your name back to the list.')



    @commands.command()
    async def fnranksdetail(self):
        """This gives the rank leaderboard with more detail than regular fnranks"""
        await self.bot.say('This command has been replaced with !fnranks. Run that command instead.')


    @commands.command(pass_context=True)
    async def fnlink(self, ctx, username):
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

    def getwinrate(self, data):
        return round(data['br']['stats']['pc']['all']['winRate'], 2)

    def getkd(self, data):
        return round(data['br']['stats']['pc']['all']['kpd'], 2)


def setup(bot):
    bot.add_cog(Fortnite(bot))
