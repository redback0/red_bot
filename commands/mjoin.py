import logging
import globs
from discord.utils import get


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'mjoin'
description = 'join a voice channel :D'
permissions = None

async def execute(bot, msg):

	channel = msg.author.voice.channel
	if not channel:
		await msg.channel.send("Join a VC so I can join you!")
		log.info(f"User is not in a VC, exitting")
	else:
		voice_client = get(bot.voice_clients, guild=msg.guild)
		if voice_client:
			if voice_client.is_connected():
				log.info("Already Connected to VC")
				await msg.channel.send("Already in VC")
			else:
				await voice_client.move_to(channel)
				await msg.channel.send("Joined VC!")
				log.info(f"Joined vc in {msg.guild.name}")
		else:
			await channel.connect(self_deaf=True)
			await msg.channel.send("Joined VC!")
			log.info(f"Joined vc in {msg.guild.name}")


