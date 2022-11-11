from commands.eco_commands.eco_common import *

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = "item"
description = "Buy, view or sell available items"
usage = f"{globs.DEF_PREFIX}eco shop [buy|sell|view] <item> [quantity=1]]"

"""
Buy sell, or view items
"""


def _show_items(embed: discord.Embed) -> None:
    """
    Adds the item fields to the provided embed.
    """

    for itemKey in Item.itemTypes.keys():
        item = Item.itemTypes[itemKey]
        embed.add_field(name=item.type, value=item.describe())


async def execute(bot, msg, path):
    # create args
    args = msg.content[msg.content.find(' ') + 1 + len(name):].split()
    log.debug(args)

    # if we have no args, display the items in the shop
    if len(args) == 0:
        shopEmbed = discord.Embed(title="Item Shop")

        # if there are no items, tell the user that
        if len(Item.itemTypes.keys()) == 0:
            shopEmbed.description = "Sorry, no items are available."

        else:

            # add each item to the discord embed
            _show_items(shopEmbed)

            # tell the user how to buy an item
            shopEmbed.description = "To buy something enter: " + \
                                    f"`{globs.DEF_PREFIX}eco shop buy <item> [quantity=1]`"

        await msg.reply(embed=shopEmbed)
        log.info("Displayed shop")
        return

    if args[0] == "view":
        # check if there is enough arguments
        if len(args) < 2:
            await msg.reply(
                f"Please specify what you'd like to view. Usage: {usage}")
            log.info("User didn't specify what to view")
            return

        # parse args[1] as itemType
        try:
            itemType = Item.itemTypes[args[1]]

        except KeyError:
            await msg.reply(f"Sorry, {args[1]} isn't a valid item")
            log.info(f"{args[1]} isn't a valid item")
            return

        # create embed
        itemEmbed = discord.Embed(title=f"{str(itemType.type).title()}")

        itemEmbed.description = itemType.description

        if itemType.buyAble:
            cost = f"${itemType.cost}"
        else:
            cost = "N/A"

        itemEmbed.add_field(name="Cost", value=cost)
        itemEmbed.add_field(name="Buy-able", value=f"{'Yes' if itemType.buyAble else 'No'}")
        itemEmbed.add_field(name="Use-able", value=f"{'Yes' if itemType.useAble else 'No'}")

        await msg.reply(embed=itemEmbed)
        log.info(f"Displayed {itemType.type}")

        return

    # check that the user specified to buy
    elif args[0] == "buy":

        # check if there's enough arguments
        if len(args) < 2:
            await msg.reply(
                f"Please specify what you'd like to buy. Usage: {usage}")
            log.info("User didn't specify what to buy")
            return

        # parse args[1] as itemType
        try:
            itemType = Item.itemTypes[args[1]]

        except KeyError:
            await msg.reply(f"That's not a valid item")
            log.info("User gave an invalid itemtype")
            return

        if not itemType.buyAble:
            await msg.reply("That item cannot be bought.")
            log.info("cannot be bought")
            return

        # parse qty if it exists, otherwise set it to 1
        if len(args) > 2:
            try:
                qty = int(args[2])

            except ValueError:
                await msg.reply("Quantity must be a number")
                log.info("User specified bad quantity")
                return

            # if we've parsed qty, make sure it's more than 1
            if qty < 1:
                await msg.reply("You must buy at least 1 item")
                log.info("User tried to buy less than 1 item")
                return

        else:
            qty = 1

        # get userData and set totalCost
        totalCost = itemType.cost * qty
        userData = UserData.getUserData(path, msg.author)

        # check if the user has enough points
        if userData.wallet < totalCost:
            await msg.reply("You don't have enough points to do that")
            log.info("User tried to buy, but didn't have enough points")
            return

        # all cases checked, do the calculations
        userData.wallet -= totalCost

        userData.invAddItem(args[1], qty)

        await msg.reply(f"Bought {qty} x {args[1]} for {totalCost} points")
        log.info(f"User bought {qty} x {args[1]} for {totalCost}")

        userData.saveUserData(path)
        return

    elif args[0] == "sell":
        # check if there's enough arguments
        if len(args) < 2:
            await msg.reply(
                f"Please specify what you'd like to buy. Usage: {usage}")
            log.info("User didn't specify what to buy")
            return

        # parse args[1] as itemType
        try:
            itemType = Item.itemTypes[args[1]]

        except KeyError:
            await msg.reply(f"That's not a valid item")
            log.info("User gave an invalid itemtype")
            return

        # parse qty if it exists, otherwise set it to 1
        if len(args) > 2:
            try:
                qty = int(args[2])

            except ValueError:
                await msg.reply("Quantity must be a number")
                log.info("User specified bad quantity")
                return

            # if we've parsed qty, make sure it's more than 1
            if qty < 1:
                await msg.reply("You must sell at least 1 item")
                log.info("User tried to sell less than 1 item")
                return

        else:
            qty = 1

        # get userData and set totalCost
        totalCost = int(itemType.cost * qty * UserData.REFUND_RATE)
        userData = UserData.getUserData(path, msg.author)

        i = userData.searchInventory(itemType.type)

        # check if the user has enough points
        if i < 0:
            await msg.reply("You don't have any of that item")
            log.info("User tried to sell an item they don't have")
            return

        if userData.inventory[i].quantity < qty:
            await msg.reply("You don't have that much of that item")
            log.info("User tried to sell more of an item than they have")
            return

        # all cases checked, do the calculations
        userData.wallet += totalCost
        userData.invRemoveItem(args[1], qty)

        await msg.reply(f"Sold {qty} x {args[1]} and recieved {totalCost} points")
        log.info(f"User sold {qty} x {args[1]} for {totalCost}")

        userData.saveUserData(path)
        return

    # if args[1] is neither 'sell' nor 'buy'
    await msg.reply(f"Invalid option {usage}; try either `sell` or `buy`")
    log.info(f"User gave an invalid argument `{globs.DEF_PREFIX}eco shop [badArg]`")
    return
