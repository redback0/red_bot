from importlib import import_module

path = 'commands.eco_commands.'

subcmds = {
	'daily': import_module(f'{path}daily'),
	'balance': import_module(f'{path}balance'),
	'steal': import_module(f'{path}steal'),
	'deposit': import_module(f'{path}deposit'),
	'inventory': import_module(f'{path}inventory'),
	'top': import_module(f'{path}top')
}

# aliases
subcmds.update({
	'bal': subcmds['balance'],
	'rob': subcmds['steal'],
	'dep': subcmds['deposit'],
	'inv': subcmds['inventory']
})