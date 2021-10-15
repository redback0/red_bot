from importlib import import_module
path = 'commands.'

cmds = {
	#'test': import_module('commands.test'),
	'repeat': import_module(f'{path}repeat'),
	'cringe': import_module(f'{path}cringe'),
	'server': import_module(f'{path}server'),
	'eco': import_module(f'{path}eco')
}

