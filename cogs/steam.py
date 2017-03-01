import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import os
import json
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


def setup(bot):
	bot.add_cog(steam(bot))