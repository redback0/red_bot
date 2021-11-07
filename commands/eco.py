import os 
import traceback
import logging
import discord
import globs

import commands.eco_commands.index as ecocmd_index

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

PREFIX = globs.DEF_PREFIX

name = 'eco'
description = f'A set of economy commands. {PREFIX}eco help for more'



async def _execute(bot, msg):

	path = './commands/eco_commands/guilds/'

	if msg.guild == None:
		await msg.reply(f'Unable to use {PREFIX}eco in DMs')
		log.info('Attempted to use .eco in DMs') 
		return
	else:
		path += str(msg.guild.id) + '.json'

	log.debug(path)

	if not ' ' in msg.content:
		await msg.reply(f'Do `{PREFIX}eco help` for available commands')
		log.info('No subcommand given')
		return

	# iEndCMD, useful for shortening the next statement
	iEndCMD = msg.content.find(' ')+1
	iEndEcoCMD = msg.content[iEndCMD:].find(' ') + iEndCMD

	# find the second word in msg.content:
	# go from 1 more than the index of the first space, 
	# to the index of the next space
	if not iEndEcoCMD - iEndCMD == -1:
		subcmd = msg.content[iEndCMD:iEndEcoCMD]
	else:
		subcmd = msg.content[iEndCMD:]
	log.info(f'Subcommand: {subcmd}')


	# special case sub commands

	# help
	# loops through all ecocmds and prints their descriptions
	if subcmd == 'help':
				
		log.info('Generating help message')
		helpmsgdesc = f'{PREFIX}eco help: Displays this list\n';


		for key in ecocmd_index.ecocmds.keys():
			
			if ecocmd_index.ecocmds[key].permissions == "guilds":

				if msg.guild == None: 
					guild = None
				else: 
					guild = msg.guild.id
				log.debug(f"guild ID: {guild}")

				if not guild in ecocmd_index.ecocmds[key].guilds:
					return


			helpmsgdesc += f'{PREFIX}eco {key}: '

			# if the subcmd points to another subcmd, call it an alias
			if not ecocmd_index.ecocmds[key].name == key:
				helpmsgdesc += f'Alias for {ecocmd_index.ecocmds[key].name}\n'
			else:
				helpmsgdesc += f'{ecocmd_index.ecocmds[key].description}\n'


		helpmsg = discord.Embed(title='Eco Commands', description=helpmsgdesc)


		log.info(helpmsg)
		await msg.reply(embed=helpmsg)


		return


	# regular sub commands
	try:

		if ecocmd_index.ecocmds.get(subcmd, False):

			log.debug(ecocmd_index.ecocmds[subcmd])
			# run sub command
			await ecocmd_index.ecocmds[subcmd].execute(bot, msg, path)
			log.info(f'Sub command executed: {subcmd}')
		else:
			await msg.reply(
				'Invalid command; Do .eco help for available commands')
			log.info(f'Invalid sub command: {subcmd}')
			
	except Exception as err:

		log.warning(f'Command {subcmd} had a problem:')
		log.warning(traceback.format_exc())
		log.warning(err)




