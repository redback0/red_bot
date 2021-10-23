import os
import json
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def_userdata = {
	'wallet': 500,
	'bank': 0
}

# read JSON from a file and pick the dictionary with the key userID
def readFile(path, userID):

	log.debug(f'path:{path}, userID:{userID}')
	# check the file exists, if it doesn't, create a default profile
	if os.path.isfile(path):
		with open(path, mode='rt', encoding='utf-8') as file:
			data = json.load(file)

		log.info('read from file')
		log.debug(data.keys())
		log.debug(data.get(userID))
		return data.get(userID, def_userdata)

	log.info(f'file did not exist, using defualt')
	return def_userdata

def readAll(path):

	if os.path.isfile(path):
		with open(path, mode='rt', encoding='utf-8') as file:
			data = json.load(file)

		log.info('read from file')
		return data

	log.info('file did not exist, returning null')
	return


# writes userdata to a file
def writeFile(path, userdata):

	# set commonly changed values
	log.debug(userdata)
	for key in userdata.keys():

		# set walletMax
		if userdata[key].get('walletMax', 0) < userdata[key]['wallet']:
			userdata[key]['walletMax'] = userdata[key]['wallet']

	# check if the file exists
	# file doesn't exist
	if not os.path.isfile(path):
		# the file doesn't exist; create it, write in userdata

		# --- THIS SHOULD NOT BE A STRING, SHOULD CALL TO A VARIABLE ---
		folder = path[:path.rfind('/')]
		if not os.path.exists(folder):
			os.mkdir(folder)
			log.debug(f'Created folder: {folder}')

		with open(path, mode='x', encoding='utf-8') as file:
			json.dump(userdata, file, indent=4)
			log.info(f'Created and wrote to file: {path}')

	# file does exist
	else:
		# the file does exist; read it, insert new userdata, write to file
		with open(path, mode='r+t', encoding='utf-8') as file:
			# read file then move buffer back to the bigining
			data = json.load(file)
			file.seek(0)

			# write in userdata
			data.update(userdata)
			# write to file
			log.debug(json.dumps(data))
			json.dump(data, file, indent=4)
			file.truncate()
			log.info(f'Wrote to existing file: {path}')
