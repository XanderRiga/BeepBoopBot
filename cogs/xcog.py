import discord
from discord.ext import commands
import urllib
from urllib.request import urlopen

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import aiohttp

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xander(self):

        #Prints all Xander face emojis in a line
        await self.bot.say("<:xhearteyes:283866074980810752> <:xandercool:235634201678839809> <:xandertilted:235633458779521024> <:xander:235610087190822913> <:hueh:235633477179932672> <:LUL:235611940590845952> <:xhearteyes:283866074980810752>")

    @commands.command(pass_context=True)
    async def echo(self, ctx, message):

        author = ctx.message.author
        myString = ctx.message.content
        await self.bot.say("{} {}".format(author.mention, myString[6:]))

    @commands.command()
    async def rlnow(self):
        """How many players are online atm?"""

        #Your code will go here
        url = "https://steamdb.info/app/252950/graphs/" #build the web adress
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            online = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
            await self.bot.say(online + ' players are playing Rocket League at the moment')
        except:
           await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")


    @commands.command()
    async def hours(self, user):
        """Returns hours played by a user"""

        #link = user
        #substringCheck = "https://steamcommunity.com/profiles/"
        #substringCheck2 = "https://steamcommunity.com/id/"
        #if substringCheck in link:
        #    url = link + "/games/?tab=all"  # build the web address
        #if substringCheck2 in link:
        #    url = link + "/games/?tab=all"  # build the web address
        #else:
        #    url = substringCheck2 + link + "/games/?tab=all"

        url = "http://steamcommunity.com/id/xanderdagr8/games/?tab=all"

        #await self.bot.say(url)
        async with aiohttp.get(url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            #await self.bot.say(soup.renderContents())
        try:
            name_box = soup.find('h5').get_text()
            await self.bot.say(name_box)
        except:
           await self.bot.say("This user does not own Rocket League")



def setup(bot):
	if soupAvailable:
		bot.add_cog(Mycog(bot))
	else:
		raise RuntimeError("You need to run `pip3 install beautifulsoup4`")