import logging
import globs
import discord
from discord.utils import get

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'play'
description = 'plays audio :)'
permissions = "creator"

async def execute(bot, msg):

	voice_client = get(bot.voice_clients, guild=msg.guild)

	if voice_client and voice_client.is_connected():
		source = await discord.FFmpegOpusAudio.from_probe("audio/test.mp3")
		voice_client.play(source)
