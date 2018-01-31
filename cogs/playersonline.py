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

        finalString = ""

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
            finalString += str(gamesBeingPlayed[x]) + " player(s) playing " + x + "\n"

        await self.bot.say(finalString)

    #This will give player who calls the command the role for the specified game
    @commands.command(pass_context=True)
    async def role(self, ctx, game):
        game = game.lower()
        if game != "br" and game != "overwatch":
            await self.bot.say("Currently the only games you can add roles for are \"overwatch\" and \"br\"")
            return

        author = ctx.message.author

        # MUST SET SERVER ID BACK TO WCU AFTER: 174382936877957120
        server = discord.utils.find(lambda m: m.id == '174382936877957120', self.bot.servers)
        if game == "br":
            role = discord.utils.find(lambda m: m.name == game.upper(), server.roles)
        if game == "overwatch":
            role = discord.utils.find(lambda m: m.name == game.capitalize(), server.roles)

        for x in author.roles:
            if(role == x):
                await self.bot.remove_roles(author, role)
                await self.bot.say("You have removed " + game + " from your roles")
                return

        await self.bot.add_roles(author, role)
        await self.bot.say("You have given yourself the " + game + " role")


def setup(bot):
    bot.add_cog(playersonline(bot))