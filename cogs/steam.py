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
		self.allRanks = ["Unranked", "Bronze 1", "Bronze 2", "Bronze 3", "Silver 1", "Silver 2", "Silver 3", "Gold 1", "Gold 2", "Gold 3", "Platinum 1", "Platinum 2", "Platinum 3", "Diamond 1", "Diamond 2", "Diamond 3", "Champion 1", "Champion 2", "Champion 3", "Grand Champion"]

	@commands.command(pass_context=True)
	async def relinksteam(self, ctx, reguser : discord.Member, steamID):
		"""Use this to link a user's Steam ID to their Discord"""
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
			await self.bot.say( "Congrats, your rank updated! Check your roles." )
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
				i+=1
				if not bool:
					self.bot.say("Failed to update on: " + str(i) + " aka " + discordID )

		await self.bot.say("Success: " + str(i) + " profile(s) updated")

	#What happens behind the scenes
	async def updateBTS(self, discordID):

		if discordID not in self.steamList:
			await self.bot.say("Your steam is not linked. use !linksteam to get your rank")
			return false

		url = "https://rocketleague.tracker.network/profile/steam/" + self.steamList[discordID]
		picArr = []
		rankArr = []
		highestRank = 0

		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")
		try:
			for tag in soup.contents[3].body.find(class_='container content-container').find(class_='card-table items').find_all('img'):
				temp2 = (tag.get('src'))
				#await self.bot.say(temp2)
				picArr.append(temp2)

			for x in picArr:
				#This makes an array of just the numbers in the URLs. Each one is a list of 2, the first is always 4, the 2nd is the number I want
				rankArr.append(re.findall("\d+", x))
				#await self.bot.say(re.findall("\d+", x))

			#await self.bot.say(rankArr)

			index = 0
			for x in rankArr:
				rankArr[index] = int(x[1])
				index += 1

			highestRank = max(rankArr)
			#await self.bot.say(highestRank)

		except:
			await self.bot.say("Couldn't load mmr. Is rocketleague.tracker.network offline?")

		if (highestRank == 0):
			rank = "Unranked"
		elif (highestRank == 1):
			rank = "Bronze 1"
		elif (highestRank == 2):
			rank = "Bronze 2"
		elif (highestRank == 3):
			rank = "Bronze 3"
		elif (highestRank == 4):
			rank = "Silver 1"
		elif (highestRank == 5):
			rank = "Silver 2"
		elif (highestRank == 6):
			rank = "Silver 3"
		elif (highestRank == 7):
			rank = "Gold 1"
		elif (highestRank == 8):
			rank = "Gold 2"
		elif (highestRank == 9):
			rank = "Gold 3"
		elif (highestRank == 10):
			rank = "Platinum 1"
		elif (highestRank == 11):
			rank = "Platinum 2"
		elif (highestRank == 12):
			rank = "Platinum 3"
		elif (highestRank == 13):
			rank = "Diamond 1"
		elif (highestRank == 14):
			rank = "Diamond 2"
		elif (highestRank == 15):
			rank = "Diamond 3"
		elif (highestRank == 16):
			rank = "Champion 1"
		elif (highestRank == 17):
			rank = "Champion 2"
		elif (highestRank == 18):
			rank = "Champion 3"
		elif (highestRank == 19):
			rank = "Grand Champion"
		else:
			rank = "0"

		self.rankList[discordID] = rank
		dataIO.save_json("data/rank/rank.json", self.rankList)

		#MUST SET SERVER ID BACK TO WCU AFTER
		server = discord.utils.find(lambda m: m.id=='174382936877957120', self.bot.servers)
		member = discord.utils.find(lambda m: m.id== discordID, server.members)
		role = discord.utils.find(lambda m: m.name == rank, server.roles)

		ranksToRemove = []
		userRoles = []

		for z in member.roles:
			userRoles.append(z.name)

		for x in self.allRanks:
			#await self.bot.say(x)
			if x in userRoles:
				#await self.bot.say("it should append a role now")
				ranksToRemove.append(x)

		try:
			for x in ranksToRemove:
				tempRank = discord.utils.find(lambda m: m.name == x, server.roles)
				await self.bot.remove_roles(member, tempRank)
		except:
			pass

		await self.bot.add_roles(member, role)


		return True

def setup(bot):
	bot.add_cog(steam(bot))