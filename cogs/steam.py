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

	@commands.command(pass_context=True)
	async def relinksteam(self, ctx, reguser : discord.Member, steamID):
		"""Use this to link a user's Steam ID to their Discord"""
		author = ctx.message.author
		
		admin_role = settings.get_server_admin(self.server)
		mod_role = settings.get_server_mod(self.server)
		is_admin = discord.utils.get(author.roles, name=admin_role) is not None
		is_mod = discord.utils.get(author.roles, name=mod_role) is not None
		
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
		author = ctx.message.author
		discordID = ctx.message.author.id

		if discordID in self.steamList:
			rank = await self.updateBTS(discordID)
		else:
			await self.bot.say("Your steam is not linked. use !linksteam to get your rank")
			return

		self.rankList[discordID] = rank
		dataIO.save_json("data/rank/rank.json", self.rankList)

		#id on next line needs to be replaced with server id
		server = discord.utils.find(lambda m: m.id=='174382936877957120', self.bot.servers)
		#await self.bot.say(author.top_role.name + ': ' + rank)
		role = discord.utils.find(lambda m: m.name == rank, server.roles)
		#role = discord.Object(id='287044463400976384')
		#for x in role:
			#await self.bot.say(x.name + ": " + x.id)
		
		await self.bot.add_roles(author, role)
		await self.bot.say("Congrats! Your updated rank is: " + rank )


	#What happens behind the scenes
	async def updateBTS(self, discordID):
		url = "https://rocketleague.tracker.network/profile/steam/" + self.steamList[discordID]
		#from xcog:
		#await self.bot.say(url)
		picArr = []
		rankArr = []
		highestRank = 0

		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")
		try:
			#await self.bot.say(url)
			#await self.bot.say(len(soup.contents))
			for tag in soup.contents[3].body.find(class_='container content-container').find(class_='trn-container stats-container').find(class_='table table-striped').find_all('img'):
				#temp = ''.join(tag.get_text().split())
				temp2 = (tag.get('src'))
				#await self.bot.say(temp2)
				picArr.append(temp2)

			#await self.bot.say(picArr)
			
			for x in picArr:
				rankArr.append(re.findall("\d+", x))

			index = 0
			for x in rankArr:
				for y in x:
					rankArr[index] = int(y)
					index += 1

			#await self.bot.say(rankArr)
			highestRank = max(rankArr)
			#await self.bot.say(highestRank)

		except:
			await self.bot.say("Couldn't load mmr. Is rocketleague.tracker.network offline?")


		if (highestRank == 0):
			return "Unranked"
		if (highestRank == 1):
			return "Prospect 1"
		if (highestRank == 2):
			return "Prospect 2"
		if (highestRank == 3):
			return "Prospect 3"
		if (highestRank == 4):
			return "Prospect Elite"
		if (highestRank == 5):
			return "Challenger 1"
		if (highestRank == 6):
			return "Challenger 2"
		if (highestRank == 7):
			return "Challenger 3"
		if (highestRank == 8):
			return "Challenger Elite"
		if (highestRank == 9):
			return "Rising Star"
		if (highestRank == 10):
			return "Shooting Star"
		if (highestRank == 11):
			return "All Star"
		if (highestRank == 12):
			return "Super Star"
		if (highestRank == 13):
			return "Champion"
		if (highestRank == 14):
			return "Super Champion"
		if (highestRank == 15):
			return "Grand Champion"	
		else:
			return "0"
		
		



def setup(bot):
	bot.add_cog(steam(bot))