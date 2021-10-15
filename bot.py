import os
import sys
import logging
from importlib import reload

import discord
from dotenv import load_dotenv

# import a dictionary of all commands
# this allows me to link a string to a module
import commands.index as cmd_index

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv('TOKEN')
DEF_PREFIX = os.getenv('DEF_PREFIX')
CREATOR = int(os.getenv('CREATOR'))

log.info(f'Prefix: {DEF_PREFIX}')


class MyClient(discord.Client):
	async def on_ready(self):
		log.info(f'logged in as {self.user}')

	async def on_message(self, msg):

		# make sure the message isn't from this bot
		# or an empty message
		if msg.author == self.user or msg.content == None or msg.content == '':
			return

		if msg.content == '':
			return

		# pointless dumb command
		if msg.content == 'yo wuddup' and msg.author.id == CREATOR:
			await msg.channel.send('yo wuddup')
			log.info("said 'yo wuddup'")

		# actual useful commands
		elif msg.content[0] == DEF_PREFIX:

			# get the first word of the command, without the leading DEF_PREFIX
			if msg.content.find(' ') > 0:
				command = msg.content[1:msg.content.find(' ')]
			else:
				command = msg.content[1:]

			log.info(f'Command: {command}, called from: {msg.channel.name} \
in {msg.guild.name} by {msg.author.name}#{msg.author.discriminator}')

			# special case commands

			# help: Displays all available commands
			if command == 'help':
				
				log.info('Generating help message')
				helpmsgdesc = f'{DEF_PREFIX}help: Displays this list\n';

				if msg.guild == None: 
					guild = None
				else: 
					guild = msg.guild.id

				log.debug(guild)

				reload(cmd_index)

				for key in cmd_index.cmds.keys():
					if not cmd_index.cmds[key].servers == []:
						if not guild in cmd_index.cmds[key].servers:
							return

					helpmsgdesc += f'{DEF_PREFIX}{key}: '
					helpmsgdesc += f'{cmd_index.cmds[key].description}\n'


				helpmsg = discord.Embed(title='Commands', description=helpmsgdesc)


				log.info(helpmsg)
				await msg.channel.send(embed=helpmsg)


				return

# REWRITE THIS TO BE THE SAME AS IN eco.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			
			# regular commands
			try:
				# reload the files to be sure they're up to date
				reload(cmd_index)
				reload(cmd_index.cmds[command])

				log.debug(cmd_index.cmds[command])
				# run the command
				await cmd_index.cmds[command].execute(self, msg)
				log.info(f'Command executed: {command}')
			except Exception as e:
				log.info(f'Invalid command: {command}')
				log.debug(e)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

intents = discord.Intents().all()
intents.presences = False

log.info(intents)

client = MyClient(intents=intents)
client.run(TOKEN)