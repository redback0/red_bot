import logging
import globs
import os
import json

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'rrsetup'
description = 'Used to setup reaction roles'
permissions = "creator" # this should be "roleperms" with roleperms = "admin"

usage = f"""{globs.DEF_PREFIX}rrsetup #channel-for-message
emoji = role
emoji = role
emoji = role"""

async def execute(bot, msg):

	# make sure exactly 1 channel was mentioned
	if len(msg.channel_mentions) != 1:

		await msg.reply(f"Usage: ```{usage}```")
		return


	# make sure there where roles mentioned
	if len(msg.role_mentions) == 0:
		# ERROR MESSAGE HERE **************************************
		# tell user how to properly use command
		return


	lines = msg.content.split("\n")[1:]

	rrPairs = {}

	# go through each line, pairing emoji with roles
	for line in lines:

		columns = [c.strip(" <>@&") for c in line.split("=")]

		rrPairs[columns[0]] = columns[1]


	emojis = rrPairs.keys()

	log.debug(bot.emojis)

	"""
	for emoji in emojis:
		if not emoji in bot.emojis:
			await msg.reply(f"Invalid emoji: {emoji}")
			return
	"""

	#create the message for rr
	message = "React to get role:"


	for emoji in emojis:

		role = msg.guild.get_role(int(rrPairs[emoji]))

		message += f"\n{emoji} {role.mention}"

	sentMessage = await msg.channel_mentions[0].send(message)

	# react to the sent message with all the emoji
	for emoji in emojis: await sentMessage.add_reaction(emoji)



	#create json entry
	rrPath = "reaction_roles.json"

	# if file exists, open and dump json to data
	if os.path.isfile(rrPath):
		with open(rrPath, mode='rt', encoding='utf-16') as file:
			data = json.load(file)

	else:
		data = {}


	data[f"{msg.guild.id},{sentMessage.id}"] = rrPairs


	if not os.path.isfile(rrPath):
		with open(rrPath, mode='x', encoding='utf-16') as file:
			json.dump(data, file, indent=4)

	else:
		with open(rrPath, mode='r+', encoding='utf-16') as file:
			json.dump(data, file, indent=4)


	await msg.reply("Reaction roles added")