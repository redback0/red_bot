import datetime
import logging
import discord
from importlib import reload

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

name = 'balance'
description = 'Check your balances'
servers = []


# check the balance of a users wallet and bank
async def execute(bot, msg, path):
	reload(eco_common)

	log.debug(msg.mentions)



	if msg.mentions == []:
		user = msg.author
	else:
		user = msg.mentions[0]

	userdata = eco_common.readFile(path, str(user.id))
	log.debug(userdata)


	balances = discord.Embed(title=f'{user.name}\'s Balances')

	balances.add_field(name='Wallet', value=userdata.get('wallet'))
	balances.add_field(name='Bank', value=userdata.get('bank'))


	await msg.channel.send(embed=balances)
	log.info(balances)