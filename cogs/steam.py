import discord
from discord.ext import commands
import os
import json
import aiohttp
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False

#from discord.ext import commands

class steam:

	def __init__(self, bot):
		self.bot = bot
		self.steamList = dataIO.load_json("data/steam/steam.json")

	@commands.command(pass_context=True)
	async def linksteam(self, ctx, steamID):
		"""Use this to link your Steam ID to your Discord"""
		triggerSubtextOne = "/id/" #this is the string directly before the id in the url
		triggerSubtextTwo = "/profiles/" #this is the string directly before the id in the url
		discordID = ctx.message.author.id
		data = {}

		if "http://steamcommunity.com/id" in steamID :
			steamID = steamID[steamID.find(triggerSubtextOne)+len(triggerSubtextOne):]

		if "http://steamcommunity.com/profiles/" in steamID :
			steamID = steamID[steamID.find(triggerSubtextTwo)+len(triggerSubtextTwo):]

		if (discordID in self.steamList):
			await self.bot.say("Your Steam ID was already registered. Please contact an admin if you believe this is an error.")
		else:
			self.steamList[discordID] = steamID
			dataIO.save_json("data/steam/steam.json", self.steamList)
			await self.bot.say("Success! Your steam ID is now linked to your Discord ID.")

    #admin command to update all
	@commands.command(pass_context=True)
	async def updateall(self, ctx, user):
		is_admin = discord.utils.get(user.roles, name=admin_role) is not None
		is_mod = discord.utils.get(user.roles, name=mod_role) is not None

		if is_admin or is_mod:
			for discordID in steamList:
				updateBTS(self, discordID) 

	#command for user to update their own mmr
	@commands.command(pass_context=True)
	async def update(self, ctx):
		discordID = ctx.message.author.id
		self.bot.say( "here!")
		rank = await self.updateBTS(discordID)
		self.bot.say( "output: " + rank )

	#What happens behind the scenes
	async def updateBTS(self, discordID):
		url = "https://rocketleague.tracker.network/profile/steam/" + self.steamList[discordID]
		#from xcog:
		#await self.bot.say(url)
		async with aiohttp.get(url) as response:
			soupObject = BeautifulSoup(await response.text(), "html.parser")
		try:
			#beg = 
			standard = soupObject.find(class_='table.table-striped').find('tbody').find('tr').find('td').find('img').get_text()
			#solo     = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
			#doubles  = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
			#duel     = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
			await self.bot.say(standard)
			return standard
		except:
			await self.bot.say("Couldn't load mmr. Is rocketleague.tracker.network offline?")

		return "0"



def setup(bot):
	bot.add_cog(steam(bot))