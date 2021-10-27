import datetime
import logging
import globs
from importlib import reload

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'deposit'
description = 'Put points into your bank. You can only use this once per day'
servers = []


bankMaxMul = 5
walletMinMul = 0.1

# give a user 500 points, usable once per day
async def _execute(bot, msg, path):

	# check if there's a argument
	if not ' ' in msg.content[msg.content.find(' ')+1:]:	
		
		log.info('User did not give an amount')
		await msg.channel.send(
			'How much would you like to deposit? (`all` for maximum amount)')


	reload(eco_common)

	userdata = eco_common.readFile(path, str(msg.author.id))
	log.debug(userdata)

	user = msg.author.name + "#" + msg.author.discriminator


	today = datetime.date.today()
	maxBank = userdata.get('walletMax') * bankMaxMul
	minWallet = userdata.get('walletMax') * walletMinMul

	if minWallet < 2000:
		minWallet = 2000


	# check if the user has already done this today
	if not datetime.date.fromisoformat(
			userdata.get('lastDeposit', datetime.date.min.isoformat())) < today:

		log.info(
			f'{user} has already deposited today')
		await msg.channel.send('Sorry, you can only use this once per day')
		return

	# check if the user is able to store more in their bank
	elif userdata.get('bank') >= maxBank:
		log.info(
			f'{user}\'s bank is already full: ' +
			f'{userdata.get("bank")} >= {maxBank}')
		await msg.channel.send('Your bank is already full')
		return

	# see if the user has enough in their wallet to deposit
	elif (userdata.get('wallet') <= minWallet or 
			userdata.get('wallet') <= 2000):
		log.info(
			f'{user}\'s wallet is too empty: {userdata.get("wallet")} ' + 
			f'<= {minWallet}')
		await msg.channel.send('Your wallet is too empty for this')
		return


	maxDep = int(userdata.get('wallet') - minWallet)


	if maxDep < userdata.get('wallet') - minWallet:
		maxDep = userdata.get('wallet') - minWallet

	if maxDep > maxBank - userdata.get('bank'):
		maxDep = maxBank - userdata.get('bank')

	


	# set args list
	args = msg.content[msg.content.find(' ')+1:].split()

	log.debug(args)

	# set dep
	if args[1] == 'all':
		dep = maxDep
	else:
		try:
			dep = int(args[1])
		except ValueError:
			log.info('User entered non integer')
			await msg.channel.send(
				f'{args[1]} is not a number. ' + 
				f'Please type all, or enter the amount you\'d like to deposit')
			return

		if dep > maxDep:
			dep = maxDep

	log.info(f'Depositing {dep} points')

	# set all userdata values
	userdata['lastDeposit'] = today.isoformat()
	userdata['wallet'] -= dep
	userdata['bank'] += dep

	await msg.channel.send(f'Deposited {dep} points')

	# write userdata
	eco_common.writeFile(path, {str(msg.author.id): userdata})