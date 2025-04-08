import logging
import globs
from discord.utils import get

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'mleave'
description = 'leave a voice channel D:'
permissions = None

async def execute(bot, msg):

	voice_client = get(bot.voice_clients, guild=msg.guild)

	if voice_client and voice_client.is_connected():
		await voice_client.disconnect()
		if voice_client.is_connected():
			await msg.reply("Failed to leave VC")
			log.info("failed to leave VC")
		else:
			await msg.reply("Left VC :(")
			log.info("Left VC")

	# voiceClient doesn't exist
	else:
		await msg.reply("Not in a VC")
		log.info("Attempted to leave when not in VC")

