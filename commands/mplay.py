import logging
import globs
import discord
import os
from discord.utils import get

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'mplay'
description = 'plays audio :)'
permissions = None

async def execute(bot, msg):

	voice_client = get(bot.voice_clients, guild=msg.guild)
	

	if voice_client and voice_client.is_connected():
		if msg.content.find(' ') < 0:
			audio = "audio/default.mp3"
		else:
			audio = f"audio/{msg.content[msg.content.find(' ') + 1:]}.mp3"
		log.info(f"audio source: {audio}")
		if (os.path.isfile(audio)):
			source = await discord.FFmpegOpusAudio.from_probe(audio)
			voice_client.play(source)
		else:
			await msg.channel.send("Audio does not exist")
			log.info("File does not exist, cannot play")
	else:
		await msg.channel.send(
			f"I'm not in a VC, use {globs.DEF_PREFIX}mjoin first")
		log.info("Not in a vc, cannot play")

