import logging
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'join'
description = 'join a voice channel :D'
permissions = "creator"

async def execute(bot, msg):

	channel = msg.author.voice.channel
	if not channel:
		await msg.channel.send("Join a VC so I can join you!")
	else:
		if channel.permissions_for(msg.guild.me):
			bot.voiceClients[msg.guild.id] = await channel.connect(self_deaf=True)
			await msg.channel.send("Joined VC!")
			log.info(f"Joined vc in {msg.guild.name}")
		else:
			await msg.channel.send("I don't have permission :cry:")
			log.info(f"Unable to join VC: no permissoins")


