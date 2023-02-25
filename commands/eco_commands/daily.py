from commands.eco_commands.eco_common import *

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'daily'
description = 'Get points daily!'
servers = []


# give a user 500 points, usable once per day
async def execute(bot, msg, path):
	userData = UserData.getUserData(path, msg.author)
	log.debug(userData)

	# get today's date, to be used in the if, and to set lastDaily
	today = date.today()

	lastDaily = userData.lastDaily
	log.debug(f'lastDaily: {lastDaily}, today: {today.isoformat()}')

	if lastDaily is None:
		lastDaily = date.min
	else:
		lastDaily = lastDaily

	# check lastDaily, if it's before today wallet + 500, otherwise do nothing
	if lastDaily < today:

		# get wagerizer bonus amount

		wagerizerBonus = 0
		wagerizerInvIndex = userData.searchInventory("wagerizer")

		if wagerizerInvIndex != -1:
			wagerizerBonus += 100

		# set lastDaily then add daily amount to users wallet
		userData.lastDaily = today

		totalDeposit = UserData.dailyAmount + wagerizerBonus

		userData.wallet += totalDeposit

		await msg.reply(f'You got {totalDeposit} points! Your total is now {userData.wallet} points.')

		log.info(f'Gave {msg.author.name}#{msg.author.discriminator} 500 points')

		# write new userdata
		userData.saveUserData(path)

	else:
		await msg.reply('Oops! You\'ve already done this today, try again tomorrow!')
		log.info(f'{msg.author.name} has already claimed they\'re points')


