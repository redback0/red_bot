import logging
import globs
import discord
import os
from discord.utils import get

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'play'
description = 'plays audio :)'
permissions = "creator"

async def execute(bot, msg):

	voice_client = get(bot.voice_clients, guild=msg.guild)
	log.debug(f"{msg.content.find(' ')} == {len(msg.content)}")
	if msg.content.find(' ') < 0:
		log.info("No audio source, setting default")
		audio = "audio/default.mp3"
		#SET DEFAULT AUDIO, OR ERROR?
	else:
		audio = f"audio/{msg.content[msg.content.find(' ') + 1:]}.mp3"
	log.info(f"audio source: {audio}")

	if voice_client and voice_client.is_connected():
		if (os.path.isfile(audio)):
			source = await discord.FFmpegOpusAudio.from_probe(audio)
			voice_client.play(source)
