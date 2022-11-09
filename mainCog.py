import discord
from discord.ext import commands

class play(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('mainCog ready')

	@commands.command()
	async def cog1(self, ctx):
		await ctx.send('mainCog ready')

def setup(bot):
	bot.add_cog(play(bot))