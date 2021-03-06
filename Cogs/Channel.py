import asyncio
import discord
from   discord.ext import commands
from   operator import itemgetter
from   Cogs import Settings

# This is the admin module.  It holds the admin-only commands
# Everything here *requires* that you're an admin

class Channel:

	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		
	def message(self, message):
		# Check the message and see if we should allow it - always yes.
		# This module doesn't need to cancel messages.
		return { 'Ignore' : False, 'Delete' : False}
		
	@commands.command(pass_context=True)
	async def islocked(self, ctx):
		"""Says whether the bot only responds to admins."""
		
		isLocked = self.settings.getServerStat(ctx.message.server, "AdminLock")
		if isLocked.lower() == "yes":
			msg = 'Admin lock is *On*.'
		else:
			msg = 'Admin lock is *Off*.'
			
		await self.bot.send_message(ctx.message.channel, msg)
		
		
	@commands.command(pass_context=True)
	async def rules(self, ctx):
		"""Display the server's rules."""
		rules = self.settings.getServerStat(ctx.message.server, "Rules")
		msg = "{} Rules:\n{}".format(ctx.message.server.name, rules)
		await self.bot.send_message(ctx.message.channel, msg)
		
		
	@commands.command(pass_context=True)
	async def ismuted(self, ctx, member : discord.Member = None):
		"""Says whether a member is muted in chat."""
			
		if member == None:
			msg = 'Usage: `ismuted [member]`'
			await self.bot.send_message(ctx.message.channel, msg)
			return

		if type(member) is str:
			try:
				member = discord.utils.get(message.server.members, name=member)
			except:
				print("That member does not exist")
				return
				
		isMute = self.settings.getUserStat(member, ctx.message.server, "Muted")
		if isMute.lower() == "yes":
			msg = '{} is *Muted*.'.format(member)	
		else:
			msg = '{} is *Unmuted*.'.format(member)
			
		await self.bot.send_message(ctx.message.channel, msg)
		
	@ismuted.error
	async def ismuted_error(self, ctx, error):
		# do stuff
		msg = 'ismuted Error: {}'.format(ctx)
		await bot.say(msg)
		
		
	@commands.command(pass_context=True)
	async def listadmin(self, ctx):
		"""Lists admin roles and id's."""
		promoArray = self.settings.getServerStat(ctx.message.server, "AdminArray")
		
		# rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
		
		promoSorted = sorted(promoArray, key=itemgetter('Name'))
		
		roleText = "Current Admin Roles:\n"

		for arole in promoSorted:
			roleText = '{}**{}** (ID : `{}`)\n'.format(roleText, arole['Name'], arole['ID'])

		await self.bot.send_message(ctx.message.channel, roleText)