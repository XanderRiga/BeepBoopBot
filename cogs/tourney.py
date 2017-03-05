import challonge
import discord
from discord.ext import commands
import discord.utils

class tourney:

	def __init__(self, bot):
		self.bot = bot

	#create the tourney
	@commands.command(pass_context=True)
	async def createtourney(self, name):
		# Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
		#challonge.set_credentials("Dunkas", "CgfNVgAJM8x8IMr8dEKcKBPxEilyLKR87sGYaCD5")

		# Retrieve a tournament by its id (or its url).
		#tournament = challonge.tournaments.show(3272)

		# Tournaments, matches, and participants are all represented as normal Python dicts.
		print(tournament["id"])  # 3272
		print(tournament["name"])  # My Awesome Tournament
		print(tournament["started-at"])  # None

		# Retrieve the participants for a given tournament.
		participants = challonge.participants.index(tournament["id"])
		print(len(participants))  # 13

		# Start the tournament and retrieve the updated information to see the effects
		# of the change.
		challonge.tournaments.start(tournament["id"])
		tournament = challonge.tournaments.show(tournament["id"])
		print(tournament["started-at"])  # 2011-07-31 16:16:02-04:00

def setup(bot):
	bot.add_cog(tourney(bot))