from importlib import import_module
from commands.index import command
import logging
import globs

CREATOR = globs.CREATOR

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

path = 'commands.eco_commands.'


class eco_command(command):

	async def execute(self, bot, msg, path):

		if self.permissions == "none":
			await self._execute(bot, msg, path)
		elif self.permissions == "creator" and msg.author.id == CREATOR:
			await self._execute(bot, msg, path)
		else:
			await msg.channel.send(
				"Command failed: you don't have the necessary permissions")
			log.info(
				f"Command failed: {self.name}, " +
				f"{msg.author.name} doesn't have the necessary permissions")



ecocmds = {
	'daily': eco_command(import_module(f'{path}daily')),
	'balance': eco_command(import_module(f'{path}balance')),
	'steal': eco_command(import_module(f'{path}steal')),
	'deposit': eco_command(import_module(f'{path}deposit')),
	'inventory': eco_command(import_module(f'{path}inventory')),
	'top': eco_command(import_module(f'{path}top'))
}

# aliases
ecocmds.update({
	'bal': ecocmds['balance'],
	'rob': ecocmds['steal'],
	'dep': ecocmds['deposit'],
	'inv': ecocmds['inventory']
})