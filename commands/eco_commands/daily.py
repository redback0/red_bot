import datetime
import logging
import globs
from importlib import reload

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'daily'
description = 'Get points daily!'
servers = []


# give a user 500 points, usable once per day
async def _execute(bot, msg, path):
	reload(eco_common)

	userdata = eco_common.readFile(path, str(msg.author.id))
	log.debug(userdata)

	# get todays date, to be used in the if, and to set lastDaily
	today = datetime.date.today()


	log.debug(f'lastDaily: {userdata.get("lastDaily")}, today: {today.isoformat()}')
	# check lastDaily, if it's before today wallet + 500, otherwise do nothing
	if (datetime.date.fromisoformat(userdata.get('lastDaily', datetime.date.min.isoformat())) < today):

		#set lastDaily then add 500 to users wallet
		userdata['lastDaily'] = today.isoformat()
		userdata.update({'wallet': userdata.get('wallet', 0) + 500})
		
		await msg.channel.send(f'You got 500 points! Your total is now {userdata["wallet"]}')

		log.info(f'Gave {msg.author.name}#{msg.author.discriminator} 500 points')

		# write new userdata
		eco_common.writeFile(path, {str(msg.author.id): userdata})

	else:
		await msg.channel.send('Oops! You\'ve already done this today, try again tomorrow!')
		log.info(f'{msg.author.name}#{msg.author.discriminator} has already claimed they\'re points')