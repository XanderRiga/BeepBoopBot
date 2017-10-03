import discord
from discord.ext import commands
import os
import json
import aiohttp
import urllib
from .utils.dataIO import dataIO
from urllib.request import urlopen
import re
import operator
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
	async def listranks(self, ctx):
		"""Use this command to list all of the ranked users on the server"""

		author = ctx.message.author

		#await self.bot.say("The ranks will be listed here")

		rankNums = {}


		#assign a number for each persons rank so they can be sorted
		for x in self.rankList:
			try:
				#needs to be correct server ID for server it is used on
				server = discord.utils.find(lambda m: m.id == '174382936877957120', self.bot.servers)
				member = discord.utils.find(lambda m: m.id == x, server.members)
				if (member == None):
					continue
				#await self.bot.say(member.name)
			except:
				continue
			rank = self.rankList[x]

			rankNum = await	self.rankToNum(rank)

			rankNums[member.name] = rankNum

			#await self.bot.say("Member = " + member.name + " RankNum = " + str(rankNum))


		sorted_ranks = sorted(rankNums.items(), key=operator.itemgetter(1))
		sorted_ranks.reverse()

		rank_list_final = []

		for x in sorted_ranks:
			if (x[1] >= 1):
				rank_list_final.append(x)

		#await self.bot.say(sorted_ranks)

		finalStr = ""

		for a in rank_list_final:
			rankName = await self.numToRank(a[1])

			emojiName = rankName.replace(" ", "")
			emojiName = emojiName.lower()

			server = discord.utils.find(lambda m: m.id == '174382936877957120', self.bot.servers)
			emoji = discord.utils.find(lambda m: m.name == emojiName, server.emojis)

			if (author.name == a[0]):
				finalStr += "__**" + str(emoji) + " " + a[0] + "**__" "\n"
			else:
				finalStr += str(emoji) + " " + a[0] + "\n"

		await self.bot.say(finalStr)




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
			await self.bot.say("Success! Your steam ID is now linked to your Discord ID. Use !update to update your rank")

	#command for user to update their own mmr
	@commands.command(pass_context=True)
	async def update(self, ctx):
		discordID = ctx.message.author.id
		newRank = await self.updateBTS(discordID)

		if newRank:
			await self.bot.say("Congrats, your rank was updated to " + newRank + "!")

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
			await self.bot.say("Your steam is not linked. use !linksteam to link your steam account and see your rank")
			return False

		url = "https://rocketleague.tracker.network/profile/steam/" + self.steamList[discordID]
		picArr = []
		rankArr = []
		highestRank = 0

		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")
		try:
			for tag in soup.contents[3].body.find(class_='container content-container').find_all(class_='season-table')[0].find_all('img'):
				temp2 = (tag.get('src'))
				picArr.append(temp2)

			for x in picArr:
				#This makes an array of just the numbers in the URLs. Each one is a list of 2, the first is always 4, the 2nd is the number I want
				rankArr.append(re.findall("\d+", x))

			index = 0
			for x in rankArr:
				rankArr[index] = int(x[1])
				index += 1

			highestRank = max(rankArr)

		except:
			await self.bot.say("Couldn't load mmr. Either rocketleague.tracker.network is offline, or you linked the incorrect steam ID. Contact an admin for help if rocketleague.tracker.network is still online")
			return False

		if (highestRank == 0):
			rank = "Unranked"
		elif (highestRank == 1):
			rank = "Bronze"
		elif (highestRank == 2):
			rank = "Bronze"
		elif (highestRank == 3):
			rank = "Bronze"
		elif (highestRank == 4):
			rank = "Silver"
		elif (highestRank == 5):
			rank = "Silver"
		elif (highestRank == 6):
			rank = "Silver"
		elif (highestRank == 7):
			rank = "Gold"
		elif (highestRank == 8):
			rank = "Gold"
		elif (highestRank == 9):
			rank = "Gold"
		elif (highestRank == 10):
			rank = "Platinum"
		elif (highestRank == 11):
			rank = "Platinum"
		elif (highestRank == 12):
			rank = "Platinum"
		elif (highestRank == 13):
			rank = "Diamond"
		elif (highestRank == 14):
			rank = "Diamond"
		elif (highestRank == 15):
			rank = "Diamond"
		elif (highestRank == 16):
			rank = "Champion"
		elif (highestRank == 17):
			rank = "Champion"
		elif (highestRank == 18):
			rank = "Champion"
		elif (highestRank == 19):
			rank = "Grand Champion"
		else:
			rank = "Unranked"

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

		return rank

	async def numToRank(self, highestRank):

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
			rank = "Unranked"

		return rank


	async def rankToNum(self, rank):

		if (rank == "Unranked"):
			rankNum = 0
		elif (rank == "Bronze 1"):
			rankNum = 1
		elif (rank == "Bronze 2"):
			rankNum = 2
		elif (rank == "Bronze 3"):
			rankNum = 3
		elif (rank == "Silver 1"):
			rankNum = 4
		elif (rank == "Silver 2"):
			rankNum = 5
		elif (rank == "Silver 3"):
			rankNum = 6
		elif (rank == "Gold 1"):
			rankNum = 7
		elif (rank == "Gold 2"):
			rankNum = 8
		elif (rank == "Gold 3"):
			rankNum = 9
		elif (rank == "Platinum 1"):
			rankNum = 10
		elif (rank == "Platinum 2"):
			rankNum = 11
		elif (rank == "Platinum 3"):
			rankNum = 12
		elif (rank == "Diamond 1"):
			rankNum = 13
		elif (rank == "Diamond 2"):
			rankNum = 14
		elif (rank == "Diamond 3"):
			rankNum = 15
		elif (rank == "Champion 1"):
			rankNum = 16
		elif (rank == "Champion 2"):
			rankNum = 17
		elif (rank == "Champion 3"):
			rankNum = 18
		elif (rank == "Grand Champion"):
			rankNum = 19
		else:
			rankNum = 0

		return rankNum



def setup(bot):
	bot.add_cog(steam(bot))
