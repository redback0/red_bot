import logging
import discord
import globs
from importlib import reload

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'inventory'
description = 'View inventory contents.'
servers = []


# reply's with the inventory of the given user (default msg author)
async def _execute(bot, msg, path):
	reload(eco_common)

	log.debug(msg.mentions)


	# test if the user made any mentions, if so use the first mention
	if msg.mentions == []:
		user = msg.author
	else:
		user = msg.mentions[0]

	userdata = eco_common.readFile(path, str(user.id))
	log.debug(userdata)


	# check if the users inventory is empty
	if userdata.get('inventory') is None:
		await msg.channel.send(f'<@!{msg.author.id}>\'s inventory is empty')
		log.info('User\'s inventory is empty')
		return


	inventory = discord.Embed(title='Inventory')

	for item in userdata.get('inventory').keys():

		if type(userdata['inventory'][item]) is int:
			inventory.add_field(name=f'{userdata["inventory"]["item"]}') # idfk
			# I have to fix this once the inventory system is implemented



	await msg.channel.log(inventory)
	log.debug(inventory)
