import challonge
import discord
from discord.ext import commands
import discord.utils

class tourney:

	def __init__(self, bot):
		self.bot = bot
		self.APIkey = "CgfNVgAJM8x8IMr8dEKcKBPxEilyLKR87sGYaCD5"; #from challonge
		#challonge.set_credentials("Dunkas", self.APIkey)

	#create the tourney
	@commands.command(pass_context=True)
	async def createtourney(self, name):
		#challonge.tournaments.start(name)
		#tournament = challonge.tournaments.show(name)
		await self.bot.say( "here" )

	#allow people to enter the tourney
	@commands.command(pass_context=True)
	async def jointourney(self):
		await self.bot.say("method not defined")

	#create a bracket and begin the tourney
	@commands.command(pass_context=True)
	async def starttourney(self):
		await self.bot.say("method not defined")





