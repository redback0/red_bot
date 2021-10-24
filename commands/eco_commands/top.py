import logging
import globs
from importlib import reload
import discord

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'top'
description = 'Shows a leaderboard'
servers = []


# the leaderboard command
async def _execute(bot, msg, path):
	reload(eco_common)

	data = eco_common.readAll(path)

	# make sure there's actually information in the server
	if data is None:
		log.info('No data available for this server')
		await msg.channel.send('No information available')
		return

	worths = {}



	# calculate total value of each user
	for userID in data.keys():
		log.debug(f'adding user: {bot.get_user(int(userID))}')
		# worth = bank + wallet // in future may include some
		worth = int(data[userID]['wallet'] + data[userID]['bank'])
		worths[userID] = worth

	log.debug(worths)


	topDes = ''
	i = 0
	foundAuthor = False

	# run through users in order of worth (most to least)
	for userID in sorted(worths, key=worths.get, reverse=True):
		log.debug(f'{bot.get_user(int(userID))}: {worths[userID]}')
		i += 1

		# check if the userID is the msg author; allow exit if true
		if not foundAuthor and msg.author.id == userID:
			foundAuthor = True

		# place the top 10 users
		if i <= 10:
			topDes += f'\n{i}. {worths[userID]}, {bot.get_user(int(userID)).name}'

			if foundAuthor and i == 10:
				break

		# place the author if not in top 10
		elif foundAuthor:
			topDes += f'\n\n{i}. {worths[userID]}, {bot.get_user(int(userID)).name}'


	top = discord.Embed(title='Leaderboard', description=topDes)


	log.debug(top)
	await msg.channel.send(embed=top)



