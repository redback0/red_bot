import logging
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'leave'
description = 'leave a voice channel D:'
permissions = "creator"

async def execute(bot, msg):

	# if voiceClient exists, attempt to leave
	if bot.voiceClients.get(msg.guild.id, False):
		await bot.voiceClients[msg.guild.id].disconnect()
		if bot.voiceClients[msg.guild.id].is_connected() == True:
			await msg.channel.send("Failed to leave VC")
			log.info("Left VC")
		else:
			await msg.channel.send("Left VC :(")
			log.info("Left VC")
			bot.voiceClients.pop(msg.guild.id)

	# voiceClient doesn't exist
	else:
		await msg.channel.send("Not in a VC")
		log.info("Attempted to leave when not in VC")

