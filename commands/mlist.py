import os
import logging
import globs
import discord

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'mlist'
description = 'lists playable audio'
permissions = None

async def execute(bot, msg):

	if os.path.isdir("audio"):
		files = os.listdir("audio")
		files.remove("default.mp3")
		for file in files:
			file = file[:-4]
		if len(files) > 0:
			tracks = "```" + "\n".join(files) + "```"
			await msg.channel.send(tracks)
			log.info("listed audio tracks")
		else:
			await msg.channel.send("No tracks")
