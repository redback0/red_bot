import os
from importlib import import_module, util
import json
import logging
from datetime import *
import discord
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)


class ItemType:
    type: str
    description: str
    cost: int
    useAble: bool

    _path = "commands.eco_commands.use_item."

    def __init__(self, itemType: str, description: str, cost: int, useAble: bool) -> None:
        self._type = itemType
        self._description = description
        self._cost = cost
        self._useAble = useAble

        if util.find_spec(f"{self._path}{itemType}"):
            self.use = import_module(f'{self._path}{itemType}').use
            log.debug(f"overrode {itemType}")

    @property
    def type(self) -> str:
        return self._type

    @property
    def description(self) -> str:
        return self._description

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def useAble(self) -> bool:
        return self._useAble

    async def use(self, qty: int) -> int | None:
        log.debug("Used an item with no use")
        return -1

    def describe(self) -> str:
        return f"Cost: {self._cost}\n{self.description}"


class Item:
    """
    An item to go into UserData.inventory
    """

    type: str
    description: str
    quantity: int

    # a dictionary of all itemTypes
    # used as a reference for `.eco shop` as well as for adding items
    # as well as certain Item methods
    itemTypes = {
        # "type": ItemType("type", "description", cost)
        "stuff": ItemType("stuff", "A bunch of useless stuff (don't buy)", 100, False),
        "pickaxe": ItemType("pickaxe", "Seems kinda blunt", 5000, True),
        "wagerizer": ItemType("wagerizer", "Increases your eco daily by 100 points. Does not stack.", 15000, False)
    }

    blankItemType = ItemType("none", "This item doesn't exist", 99999999, False)

    def __init__(self, itemType: str, quantity=1):
        self._type = itemType
        self._quantity = quantity

    @property
    def type(self) -> str:
        return self._type

    @property
    def description(self) -> str:
        return self.itemTypes.get(self._type, self.blankItemType).description

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, qty: int) -> None:
        self._quantity = qty

    def describe(self):
        return f"{self.description}"


class UserData:
    """
    A set of data associated with a user, specific to guild
    """

    wallet: int
    bank: int
    walletMax: int
    lastDaily: date
    lastDeposit: date
    lastSteal: datetime
    inventory: list[Item]

    # a few values that are useful to be able to access
    bankMaxMul = 5
    walletMinMul = 0.2
    dailyAmount = 500
    minWallet = dailyAmount * 4
    REFUND_RATE = 0.5
    defUserData = {
        'wallet': minWallet,
        'bank': 0
    }

    def __init__(self, user, userData) -> None:
        self._user = user
        self._wallet = int(userData['wallet'])
        self._bank = int(userData['bank'])
        self._walletMax = int(userData.get('walletMax', self._wallet))

        if userData.get('lastDaily') is None:
            self._lastDaily = date.min
        else:
            self._lastDaily = date.fromisoformat(userData['lastDaily'])

        if userData.get('lastDeposit') is None:
            self._lastDeposit = date.min
        else:
            self._lastDeposit = date.fromisoformat(userData['lastDeposit'])

        if userData.get('lastSteal') is None:
            self._lastSteal = datetime.min
        else:
            self._lastSteal = datetime.fromisoformat(userData['lastSteal'])

        if isinstance(userData.get('inventory', None), list):
            userData['inventory'] = {}
            self._inventory = []
            return

        invList = []

        for item in userData.get('inventory', {}).keys():
            invList.append(Item(item, userData['inventory'][item]))

        # this should be a lot more complicated
        self._inventory = invList

    def toDict(self) -> dict:
        return {
            "wallet": self._wallet,
            "bank": self._bank,
            "walletMax": self._walletMax,
            "lastDaily": self._lastDaily.isoformat(),
            "lastDeposit": self._lastDeposit.isoformat(),
            "lastSteal": self._lastSteal.isoformat(),
            "inventory": self.invToDict()
        }

    def invToDict(self):
        invDict = {}

        for item in self._inventory:
            invDict[item.type] = item.quantity

        return invDict

    @property
    def user(self):
        return self._user

    @property
    def wallet(self) -> int:
        return int(self._wallet)

    @wallet.setter
    def wallet(self, wallet: int) -> None:
        self._wallet = int(wallet)

        if wallet > self._walletMax:
            self._walletMax = int(wallet)

    @property
    def bank(self) -> int:
        return int(self._bank)

    @bank.setter
    def bank(self, bank: int) -> None:
        self._bank = int(bank)

    @property
    def walletMax(self) -> int:
        return int(self._walletMax)

    @property
    def lastDaily(self) -> date:
        return self._lastDaily

    @lastDaily.setter
    def lastDaily(self, lastDaily: date) -> None:
        self._lastDaily = lastDaily

    @property
    def lastDeposit(self) -> date:
        return self._lastDeposit

    @lastDeposit.setter
    def lastDeposit(self, lastDeposit: date) -> None:
        self._lastDeposit = lastDeposit

    @property
    def lastSteal(self) -> datetime:
        return self._lastSteal

    @lastSteal.setter
    def lastSteal(self, lastSteal: datetime) -> None:
        self._lastSteal = lastSteal

    @property
    def inventory(self) -> list[Item]:
        return self._inventory

    def searchInventory(self, itemType: str) -> int:
        """
        search for all items in the inventory, if found return the index of the item, else return -1
        """
        for i, item in enumerate(self._inventory):
            if item.type == itemType:
                return i
        else:
            return -1

    def invAddItem(self, itemType: str, qty=1) -> None:
        # add an item to the inventory.
        # if the item is already in the inventory, add the quantity to the total amount.

        for i, item in enumerate(self._inventory):
            if item.type == itemType:
                # add quantity to the item
                log.debug(f"123 added {qty} to {itemType}")
                item.quantity += qty
                return
        else:
            # add the item to the inventory
            self._inventory.append(Item(itemType, qty))
            log.debug(f"123 added {itemType} to inventory")

    def invRemoveItem(self, itemType: str, qty=1) -> int:
        """
        Remove item from the inventory

        returns amount of items removed

        :return int: Amount of items removed
        """

        removedCount = 0

        for i, item in enumerate(self._inventory):
            if item.type == itemType:
                item.quantity -= qty

                if item.quantity <= 0:
                    removedCount = qty + item.quantity

                    self._inventory.remove(item)

                break

        return removedCount

    @classmethod
    def getUserData(cls, path: str, user: discord.User) -> 'UserData':

        log.debug(f'path:{path}, userID:{user.id}')
        # check the file exists, + timedelta(hours=1)f it doesn't, create a default profile
        if os.path.isfile(path):
            with open(path, mode='rt', encoding='utf-8') as file:
                data = json.load(file)

            log.info('read from file')
            log.debug(data.keys())
            userData = data.get(str(user.id), UserData.defUserData)
            log.debug(userData)

        else:
            log.info(f'file did not exist, using default')
            userData = UserData.defUserData

        return UserData(user, userData)

    @classmethod
    def getAllFromGuild(cls, bot: discord.Client, path: str):

        # check the file exists
        # if it does, read in all the userdata, then turn it into
        # UserData objects and return a list of those
        # else return an empty list
        if os.path.isfile(path):
            with open(path, mode='rt', encoding='utf-8') as file:
                data = json.load(file)
                log.info('read from file')

        else:
            log.info("file didn't exist; using empty dict")
            data = {}

        userDatas = []

        for userID in data.keys():
            userDatas.append(
                UserData(bot.get_user(int(userID)), data[userID]))

        return userDatas

    def saveUserData(self, path):

        userDatasDict = {}

        userDatasDict[str(self.user.id)] = self.toDict()
        log.debug(f"userData: {userDatasDict[str(self.user.id)]}")

        self._saveUserData(path, userDatasDict)

    @classmethod
    def _saveUserData(cls, path, userDatas):
        # check if the file exists
        # file doesn't exist
        if not os.path.isfile(path):
            # the file doesn't exist; create it, write in userdata

            folder = path[:path.rfind('/')]
            if not os.path.exists(folder):
                os.mkdir(folder)
                log.debug(f'Created folder: {folder}')

            with open(path, mode='x', encoding='utf-8') as file:
                json.dump(userDatas, file, indent=4)
                log.info(f'Created and wrote to file: {path}')

        # file does exist
        else:
            # the file does exist; read it, insert new userdata, write to file
            with open(path, mode='r+t', encoding='utf-8') as file:
                # read file then move buffer back to the beginning
                fileUserDatas = json.load(file)
                file.seek(0)

                # write in userdata
                fileUserDatas.update(userDatas)
                # write to file
                log.debug(json.dumps(fileUserDatas))
                json.dump(fileUserDatas, file, indent=4)
                file.truncate()
                log.info(f'Wrote to existing file: {path}')

    # using string for typehint as cant reference parent class in typehint without error
    @classmethod
    def saveUserDatas(cls, userDatas: list['UserData'], path: str):
        """
        save a list of userDatas to file @ path
        path:
            the file, including path, to save to
        userDatas:
            a list of UserData objects to save
        """
        userDatasDict = {}

        for userData in userDatas:
            userDatasDict[str(userData.user.id)] = userData.toDict()
            log.debug(f"userData: {userDatasDict[str(userData.user.id)]}")

        log.debug(f'dict = {userDatasDict}')

        cls._saveUserData(path, userDatasDict)
