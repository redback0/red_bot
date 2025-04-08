import logging
import globs
import os
import json

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'rrdel'
description = 'delete an existing reaction roll message'
permissions = "creator"

rrPath = "reaction_roles.json"

async def execute(bot, msg):

	msg_ids = msg.content.split(" ")[1:]

	if msg_ids == None:
		# TELL USER HOW TO USE COMMAND
		log.info("No msgs provided")
		return

	if not os.path.isfile(rrPath):
		await msg.reply("No reaction roll messages found")
		log.info("No file found")
		return
	
	with open(rrPath, mode='rt', encoding='utf-16') as file:
		data = json.load(file)

	guild_id = msg.guild.id


	for msg_link in msg_ids:
		rrchannel = await bot.fetch_channel(msg_link[-38:-20])
		rrmsg = await rrchannel.fetch_message(msg_link[-19:])

		if data.get(f"{guild_id},{msg_link[-19:]}") != None:
			del data[f"{guild_id},{msg_link[-19:]}"]
			await rrmsg.delete()
			with open(rrPath, mode='w', encoding='utf-16') as file:
				json.dump(data, file, indent=4)
			await msg.reply("Removed message")
			log.info("rr message removed")

