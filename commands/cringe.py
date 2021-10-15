import random
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

name = 'cringe'
description = "Tests the cringe level of @user"
servers = []

async def execute(bot, msg):
	if msg.content.find(' ') > 0:
		msgtrim = msg.content[msg.content.find(' ')+1:]

		if ('red_back' in msgtrim or
				'natey' in msgtrim or
				'208038162180734976' in msgtrim or
				'851816132801331260' in msgtrim):
			await msg.channel.send(f'{msgtrim} is -100% cringe')
			await msg.channel.send(f'<@!{msg.author.id}> is 100% cringe')
		elif 'red__' in msgtrim:
			await msg.channel.send("who's that?")
			await msg.channel.send(f'also <@!{msg.author.id}> is 100% cringe')
		else:
			if msg.author.id == 208038162180734976:
				chance = 100
			else:
				chance = random.randrange(101)

			await msg.channel.send(f'{msgtrim} is {chance}% cringe')
			log.info(f'cringed text: {msgtrim}')


	else:
		await msg.channel.send(f'<@!{msg.author.id}> is 100% cringe')
		log.info('Attempted to cringe, but was missing text')
