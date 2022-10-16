from importlib import import_module
import logging

import discord

import globs

CREATOR = globs.CREATOR

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

path = 'commands.'

"""
command:
	A container for a command
"""


class Command():

    def __init__(self, module) -> None:
        # set guaranteed values
        self._execute = module.execute
        self._name = module.name
        self._description = module.description

        # set other values!
        try:
            self._permissions = module.permissions

            if self.permissions == "guilds":
                try:
                    self._allowedGuilds = module.allowedGuilds

                except AttributeError:
                    self._allowedGuilds = None

            elif self.permissions == "roles":
                try:
                    self._roles = module.roles

                except AttributeError:
                    self._roles = None

            elif self.permissions == "roleperms":
                try:
                    self._rolePerms = module.roleperms

                except AttributeError:
                    self._rolePerms = None

        except AttributeError:
            self._permissions = None

    @property
    # name: the name of your command e.g. this.py would have the name "this"
    def name(self):
        return self._name

    @property
    # description: a short description of the command
    def description(self):
        return self._description

    @property
    # permissions: what permission level is required to run the command, can be
    # "guilds", "roles", or "creator"
    def permissions(self):
        return self._permissions

    # guilds: what guilds the command can be used in: requires permissions
    # to be set to "guilds"
    @property
    def allowedGuilds(self):
        return self._allowedGuilds

    # roles: what roles are allowed to use the command: requires permissions
    # to be set to "roles"
    @property
    def roles(self):
        return self._roles

    def check_perms(self, msg: discord.Message) -> bool:
        """
        Checks whether the user has permission to run the command
        """

        if self.permissions is None:
            return True

        elif msg.author.id == CREATOR:
            return True

        elif self.permissions == "guilds":
            if msg.guild is None:
                guild = None

            else:
                guild = msg.guild.id

            log.debug(f"guild ID: {guild}")

            if self.allowedGuilds is None:
                return False

            if guild in self.allowedGuilds:
                return True

        elif self.permissions == "roles":
            # roles permission is not yet implemented
            pass

        elif self.permissions == "roleperms":
            # not yet implemented
            pass

        return False

    async def execute(self, bot, msg):
        """
        Execute the command if permissions are met
        """

        log.info(f"checking perms for command {self.name}")

        # if check_perms is true, excute command
        if self.check_perms(msg):
            await self._execute(bot, msg)
        else:
            await msg.channel.send(
                "Command failed: you don't have the necessary permissions")
            log.info(
                f"Command failed: {self.name}, " +
                f"{msg.author.name} doesn't have the necessary permissions")


# dictionary that associates a string with a command instance
cmds = {
    'test': Command(import_module(f'{path}test')),
    'repeat': Command(import_module(f'{path}repeat')),
    'cringe': Command(import_module(f'{path}cringe')),
    'server': Command(import_module(f'{path}server')),
    'eco': Command(import_module(f'{path}eco')),
    'script': Command(import_module(f'{path}script')),
    'rrsetup': Command(import_module(f'{path}rrsetup'))
}
