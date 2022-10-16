from commands.eco_commands.eco_common import *
import logging
import discord
import globs

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'gift'
description = 'Gift a user an item.'
usage = f"{globs.DEF_PREFIX}eco gift <@user> <item> [amount]"
permissions = "guilds"


async def execute(bot: discord.Client, msg: discord.Message, path: str) -> None:
    # get command string. Includes bot prefix, 'eco', and command name.
    commandStr = msg.content

    # remove bot prefix, eco and command name
    commandStr = commandStr.lstrip(f"{globs.DEF_PREFIX}eco {name} ")

    # get args
    args = commandStr.split()

    # there should only be 2 - 3 args

    if len(args) < 2:
        log.info(f"Bad args: to little args ({len(args)}")
        await msg.reply(f"Usage: `{usage}`")
        return

    if len(args) > 3:
        log.info(f"Bad args: to many args ({len(args)})")
        await msg.reply(f"Usage: `{usage}`")
        return

    userMentions = msg.mentions
    if len(userMentions) > 1 or len(userMentions) < 1:
        log.info("Bad args: no user mentions / too many user mentions")
        await msg.reply(f"Usage: `{usage}`")
        return

    # check arg types and assign variables

    giftedUser = userMentions[0]

    item = args[1].lower()

    if not Item.itemTypes.get(item, False):
        log.info("Unknown item")
        await msg.reply(f"Oops! You named an item that doesn't exist: `{item}`")
        return

    if len(args) == 3:
        try:
            amount = int(args[2])
        except ValueError:
            log.info("Amount is not a number")
            await msg.reply(f"Please use a positive integer greater than 0, not `{args[2]}`.")
            return

        if amount < 1:
            log.info("Amount is less than 1")
            await msg.reply(f"Please use a positive integer greater than 0, not `{args[2]}`.")
            return

    else:
        amount = 1

    # gifted user, item, amount

    # check if the gifter has that item with the specified amount

    gifterData = UserData.getUserData(path, msg.author)

    if gifterData.searchInventory(item) == -1:
        # user does not have item
        log.info("gifter does not have item")
        await msg.reply(f"You do not have that item to gift.")
        return

    elif gifterData.searchInventory(item) < amount:
        # user does not have enough item
        log.info("gifter does not have enough items")
        await msg.reply("You do not have enough items to gift!")
        return

    giftedData = UserData.getUserData(path, giftedUser)

    # remove item from gifter
    gifterData.invRemoveItem(item, amount)

    # add item to gifted
    giftedData.invAddItem(item, amount)

    # save both gifted and gifter
    giftedData.saveUserData(path)
    gifterData.saveUserData(path)

    # success
    log.info(f"user {msg.author} gave {giftedUser} {amount}x {item}.")

    await msg.reply(f"You gave {giftedUser} `{amount}`x `{item}`!")
    return




