import discord
from discord.ext import commands
import os
import json
import aiohttp
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
import re
import discord.utils
from __main__ import send_cmd_help, settings

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
		self.rankList = dataIO.load_json("data/rank/rank.json")
		self.server = discord.utils.find(lambda m: m.id=='174382936877957120', self.bot.servers)
		self.admin_role = settings.get_server_admin(self.server)
		self.mod_role = settings.get_server_mod(self.server)

	@commands.command(pass_context=True)
	async def relinksteam(self, ctx, reguser : discord.Member, steamID):
		"""Use this to link a usser's Steam ID to their Discord"""
		author = ctx.message.author
		
		is_admin = discord.utils.get(author.roles, name=self.admin_role) is not None
		is_mod = discord.utils.get(author.roles, name=self.mod_role) is not None
		
		if is_admin or is_mod:
			i = 0 #User is a mod or Admin and can use this command
		else:
			await self.bot.say("You do not have permissions to do this. Please contact a Moderator or Director")
			return #exits as they should not be allowed to use this

		triggerSubtextOne = "/id/" #this is the string directly before the id in the url
		triggerSubtextTwo = "/profiles/" #this is the string directly before the id in the url
		discordID = reguser.id
		data = {}

		if "http://steamcommunity.com/id" in steamID :
			steamID = steamID[steamID.find(triggerSubtextOne)+len(triggerSubtextOne):]

		if "http://steamcommunity.com/profiles/" in steamID :
			steamID = steamID[steamID.find(triggerSubtextTwo)+len(triggerSubtextTwo):]

		self.steamList[discordID] = steamID
		dataIO.save_json("data/steam/steam.json", self.steamList)
		await self.bot.say("Success! Your steam ID is now linked to your Discord ID.")


	@commands.command(pass_context=True)
	async def linksteam(self, ctx, steamID):
		"""Use this to link others Steam IDs to their Discord"""
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

	#command for user to update their own mmr
	@commands.command(pass_context=True)
	async def update(self, ctx):
		discordID = ctx.message.author.id
		bool = await self.updateBTS(discordID)

		if bool:
			await self.bot.say( "Congrats your rank updated! Check your roles." )
		else:
			await self.bot.say("Your steam is not linked. use !linksteam to get your rank")

	#admin command to update all
	@commands.command(pass_context=True)
	async def updateall(self, ctx):
		author = ctx.message.author
		is_admin = discord.utils.get(author.roles, name=self.admin_role) is not None

		i = 0
		if is_admin:
			for discordID in self.steamList:
				bool = await self.updateBTS(discordID)
				await self.bot.say("Here 1")
				i+=1
				if not bool:
					self.bot.say("Failed to update on: " + str(i) + " aka " + discordID )

		await self.bot.say("Success: " + str(i) + " profile(s) updated")

	#What happens behind the scenes
	async def updateBTS(self, discordID):
		url = "https://rocketleague.tracker.network/profile/steam/" + self.steamList[discordID]
		picArr = []
		rankArr = []
		highestRank = 0

		if discordID not in self.steamList:
			await self.bot.say("Your steam is not linked. use !linksteam to get your rank")
			return false

		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")
		try:
			for tag in soup.contents[3].body.find(class_='container content-container').find(class_='trn-container stats-container').find(class_='table table-striped').find_all('img'):
				temp2 = (tag.get('src'))
				picArr.append(temp2)
			
			for x in picArr:
				rankArr.append(re.findall("\d+", x))

			index = 0
			for x in rankArr:
				for y in x:
					rankArr[index] = int(y)
					index += 1

			highestRank = max(rankArr)

		except:
			await self.bot.say("Couldn't load mmr. Is rocketleague.tracker.network offline?")

		if (highestRank == 0):
			rank = "Unranked"
		if (highestRank == 1):
			rank = "Prospect 1"
		if (highestRank == 2):
			rank = "Prospect 2"
		if (highestRank == 3):
			rank = "Prospect 3"
		if (highestRank == 4):
			rank = "Prospect Elite"
		if (highestRank == 5):
			rank = "Challenger 1"
		if (highestRank == 6):
			rank = "Challenger 2"
		if (highestRank == 7):
			rank = "Challenger 3"
		if (highestRank == 8):
			rank = "Challenger Elite"
		if (highestRank == 9):
			rank = "Rising Star"
		if (highestRank == 10):
			rank = "Shooting Star"
		if (highestRank == 11):
			rank = "All Star"
		if (highestRank == 12):
			rank = "Super Star"
		if (highestRank == 13):
			rank = "Champion"
		if (highestRank == 14):
			rank = "Super Champion"
		if (highestRank == 15):
			rank = "Grand Champion"
		else:
			rank = "0"

		await self.bot.say( "Here, rank = " + rank ) # DEBUGGING DELETE ME

		self.rankList[discordID] = rank
		dataIO.save_json("data/rank/rank.json", self.rankList)

		server = discord.utils.find(lambda m: m.id=='174382936877957120', self.bot.servers)
		member = discord.utils.find(lambda m: m.id== discordID, server.members)

		await self.bot.add_roles(member, role)

		return true;

def setup(bot):
	bot.add_cog(steam(bot))