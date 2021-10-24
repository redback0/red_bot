import os
from importlib import import_module
import logging
import globs

CREATOR = globs.CREATOR

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)


path = 'commands.'



class command():
	"""
	command:
		A container for a command
	"""
	def __init__(self, module):
		# set garanteed values
		self.module = module
		self._execute = module._execute
		self.name = module.name
		self.description = module.description

		# set other values!
		try:
			self.permissions = module.permissions
		except:
			self.permissions = "none"

		if self.permissions == "guilds":
			try:
				self.guilds = module.guilds
			except:
				self.guilds = []

		elif self.permissions == "roles":
			try:
				self.roles = module.guilds
			except:
				self.roles = []


	async def execute(self, bot, msg):

		if self.permissions == "none":
			await self._execute(bot, msg)
		elif self.permissions == "creator" and msg.author.id == CREATOR:
			await self._execute(bot, msg)
		else:
			await msg.channel.send(
				"Command failed: you don't have the necessary permissions")
			log.info(
				f"Command failed: {self.name}, " +
				f"{msg.author.name} doesn't have the necessary permissions")



# dictionary that associates a string with a command instance
cmds = {
	'test': command(import_module(f'{path}test')),
	'repeat': command(import_module(f'{path}repeat')),
	'cringe': command(import_module(f'{path}cringe')),
	'server': command(import_module(f'{path}server')),
	'eco': command(import_module(f'{path}eco')),
	'script': command(import_module(f'{path}script'))
}

