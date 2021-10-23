import datetime
import random
import math
import logging
from importlib import reload

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

name = 'steal'
description = 'Steal points from another player'
servers = []


MIN_WALLET = 2000


# steal points from another player
async def execute(bot, msg, path):
	reload(eco_common)

	if msg.mentions == []:
		await msg.channel.send('Who are you stealing from? usage: `.eco steal <@user>`')
		log.info('no user to steal from')
		return
	elif msg.mentions[0] == msg.author:
		await msg.channel.send('You can\'t steal from yourself!')
		log.info('user tried to steal from themself')
		return


	stealerdata = eco_common.readFile(path, str(msg.author.id))
	log.debug(f'stealer: {stealerdata}')

	now = datetime.datetime.today()


	log.debug(f'lastSteal: {stealerdata.get("lastSteal")}, now: {now.isoformat()}')
	# check lastSteal, if it's been less then an hour, return
	if (datetime.datetime.fromisoformat(
			stealerdata.get('lastSteal', datetime.datetime.min.isoformat())) + 
			datetime.timedelta(hours=1) <
			now):
		
		# set lastSteal to now
		stealerdata['lastSteal'] = now.isoformat()

		# read data of the user to steal from
		stealeedata = eco_common.readFile(path, str(msg.mentions[0].id))
		log.debug(f'Stealee: {stealeedata}')

		if stealeedata['wallet'] < MIN_WALLET:
			log.info('not enough in stealee\'s wallet')
			await msg.channel.send('Try stealing from someone who has points')
			return
		elif stealerdata['wallet'] < MIN_WALLET / 2:
			log.info('stealer wallet < 1000, setting succChance to 70%')	
			succChance = 70
		else:
			log.info('stealer wallet > 1000, setting succChance to 45%')
			succChance = 55
		
		failChance = 80


		# get a number to decide if we succeed, fail, do nothing or bonus
		result = random.randrange(100)


		if result < succChance:

			percent = _percent()
			log.debug(percent)


			# choose which wallet we get the amount from
			if stealerdata['wallet'] > stealeedata['wallet']:
				steal = int(stealeedata['wallet'] * percent)
				log.debug(
					f'using stealee wallet: {stealeedata["wallet"]} * {percent} = {steal}')
			else:
				steal = int(stealerdata['wallet'] * percent)
				log.debug(
					f'using stealer wallet: {stealerdata["wallet"]} * {percent} = {steal}')


			# set the new values
			stealerdata['wallet'] += steal
			stealeedata['wallet'] -= steal


			log.info(f'Steal success: stealing {steal} points')
			await msg.channel.send(
				f'success, stealing {steal} points from <@!{msg.mentions[0].id}>')


		elif result < failChance:


			percent = _percent()

			log.debug(percent)


			# choose which wallet we get the amount from
			if stealerdata['wallet'] > stealeedata['wallet']:
				steal = int(stealeedata['wallet'] * percent)
				log.debug(
					f'using stealee wallet: '
					f'{stealeedata["wallet"]} * {percent} = {steal}')
			else:
				steal = int(stealerdata['wallet'] * percent)
				log.debug(
					f'using stealer wallet: {stealerdata["wallet"]} * {percent} = {steal}')


			# set the new values
			stealerdata['wallet'] -= steal
			stealeedata['wallet'] += steal


			log.info(f'Steal fail: stealing -{steal} points')
			await msg.channel.send(
				f'oops, got caught, you gave {steal} points to <@!{msg.mentions[0].id}>')

		# 10% chance to do nothing
		elif result < 90:

			log.info(f'Steal failed: Nothing happened')
			await msg.channel.send(f'You broke in, but forgot to steal anything')

		# 5% chance for bonus
		else:
			# something that's uncommon but increadibly undesirable
			# shouldn't change wallet, and shouldn't effect things with a cooldown
			# once .eco inv is implemented, this will actually do something interesting
			log.warning('BONUS UNIMPLEMENTED')
			await msg.channel.send('Bonus: Unimplemented')
			return


		# write new userdata
		log.debug('Writing userdata')
		eco_common.writeFile(path, {
				str(msg.author.id): stealerdata, 
				str(msg.mentions[0].id): stealeedata})

	else:
		minutes = 60 - math.floor((now - (datetime.datetime.fromisoformat(
			stealerdata["lastSteal"]))).seconds / 60)
		log.info(f'Steal failed: Hasn\'t been an hour, {minutes} minutes left')
		await msg.channel.send(f'Oops! You have to wait another {minutes} minutes')


def _percent():

	# get a percentage between 1% and 50%, distributed on the low end
	p1 = int((random.random() * 2.7) + 1)
	p2 = int((random.random() * 2.7) + 1)
	p3 = int((random.random() * 2.7) + 1)

	return (p1 * p2 * p3 / 100)
