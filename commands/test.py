import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

name = 'test'
description = 'a test command'
servers = []

async def execute(bot, msg):
	await msg.channel.send('Test successful')
	log.info('sent message: Test successful')