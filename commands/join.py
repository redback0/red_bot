import logging
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'join'
description = 'join a voice channel :D'
permissions = "creator"

async def execute(bot, msg):
	voice_channel = msg.author.voice.channel
	bot.voiceClients[msg.guild.id] = await voice_channel.connect(self_deaf=True)
	await msg.channel.send("Joined VC!")
	log.info(f"Joined vc in {msg.guild.name}")

