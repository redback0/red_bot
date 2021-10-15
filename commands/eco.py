import os 
import traceback
import logging
import discord
from importlib import reload

import commands.eco_commands.index as subcmd_index

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


name = 'eco'
description = 'A set of economy commands. .eco help for more'
servers = []


PREFIX = '.'

async def execute(bot, msg):

	path = './commands/eco_commands/guilds/'

	if msg.guild == None:
		await msg.channel.send('Unable to use .eco in DMs')
		log.info('Attempted to use .eco in DMs') 
		return
	else:
		path += str(msg.guild.id) + '.json'

	log.debug(path)

	if not ' ' in msg.content:
		await msg.channel.send('Do `.eco help` for available commands')
		log.info('No subcommand given')
		return

	# create args, a list of words after the command
	args = msg.content[msg.content.find(' ')+1:].split()

	subcmd = args[0]
	log.info(f'Subcommand: {subcmd}')
	# need more stuff here

	# help
	# loops through all subcmds and prints their descriptions
	if subcmd == 'help':
				
		log.info('Generating help message')
		helpmsgdesc = f'{PREFIX}eco help: Displays this list\n';

		if msg.guild == None: 
			guild = None
		else: 
			guild = msg.guild.id

		log.debug(guild)

		# reload the index to make sure we have the most recent version
		reload(subcmd_index)

		for key in subcmd_index.subcmds.keys():
			reload(subcmd_index.subcmds[key])
			
			if not subcmd_index.subcmds[key].servers == []:
				if not guild in subcmd_index.subcmds[key].servers:
					return

			helpmsgdesc += f'{PREFIX}eco {key}: '

			# if the subcmd points to another subcmd, call it an alias
			if not subcmd_index.subcmds[key].name == key:
				helpmsgdesc += f'Alias for {subcmd_index.subcmds[key].name}\n'
			else:
				helpmsgdesc += f'{subcmd_index.subcmds[key].description}\n'


		helpmsg = discord.Embed(title='Eco Commands', description=helpmsgdesc)


		log.info(helpmsg)
		await msg.channel.send(embed=helpmsg)


		return

	try:
		# reload the dictionary
		reload(subcmd_index)

		if subcmd_index.subcmds.get(subcmd, False):

			# reload modules before use
			reload(subcmd_index.subcmds[subcmd])

			log.debug(subcmd_index.subcmds[subcmd])
			# run sub command
			await subcmd_index.subcmds[subcmd].execute(bot, msg, path)
			log.info(f'Sub command executed: {subcmd}')
		else:
			await msg.channel.send('Invalid command; Do .eco help for available commands')
			log.info(f'Invalid sub command: {subcmd}')
	except Exception as err:

		log.warning(traceback.format_exc())
		log.warning(err)

		log.warning(f'Command {subcmd} had a problem:')



