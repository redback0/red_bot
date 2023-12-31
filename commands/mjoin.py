import logging
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'mjoin'
description = 'join a voice channel :D'
permissions = "creator"

async def execute(bot, msg):

	channel = msg.author.voice.channel
	if not channel:
		await msg.channel.send("Join a VC so I can join you!")
		log.info(f"User is not in a VC, exitting")
	else:
		await channel.connect(self_deaf=True)
		await msg.channel.send("Joined VC!")
		log.info(f"Joined vc in {msg.guild.name}")


