import discord
from discord.ext import commands
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
import requests
import aiohttp
import operator
import time


class Xander:
    """This is for xander's personal use. Pls no use"""

    def __init__(self, bot):
        self.bot = bot
        self.data = dataIO.load_json("data/xander/xander.json")

    @commands.command(pass_context=True)
    async def light(self, ctx, cmd):
        """Call this command with your username to link your discord account to your fortnite account in this server"""
        key = self.data['key']
        discordID = self.data['discordId']
        userId = ctx.message.author.id

        if discordID != userId:
            await self.bot.say('Good try pal :)')
            return

        if cmd == 'flash':
            try:
                self.lightflash(key)
                await self.bot.say('Successfully flashed the lights')
            except:
                await self.bot.say('Something went wrong, whoops!')
                return
        else:
            try:
                data = requests.get('https://maker.ifttt.com/trigger/' + cmd + '/with/key/' + key)
                if data.status_code != 200:
                    raise Exception
            except:
                await self.bot.say('That doesn\'t seem to be a valid command, try again')
                return

            await self.bot.say('Successfully completed command: ' + cmd)


    def lightflash(self, key):
        try:
            requests.get('https://maker.ifttt.com/trigger/turn_red/with/key/' + key)
            time.sleep(1)
            requests.get('https://maker.ifttt.com/trigger/on/with/key/' + key)
            time.sleep(4)
            requests.get('https://maker.ifttt.com/trigger/off/with/key/' + key)
            time.sleep(4)
            requests.get('https://maker.ifttt.com/trigger/on/with/key/' + key)
            time.sleep(4)
            requests.get('https://maker.ifttt.com/trigger/off/with/key/' + key)
            time.sleep(4)
            requests.get('https://maker.ifttt.com/trigger/on/with/key/' + key)
            time.sleep(4)
            requests.get('https://maker.ifttt.com/trigger/off/with/key/' + key)
            return
        except:
            raise Exception('something went wrong!')



def setup(bot):
    bot.add_cog(Xander(bot))
