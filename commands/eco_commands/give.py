import logging
import globs

import commands.eco_commands.eco_common as eco_common

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(globs.LOGLEVEL)

name = 'give'
description = 'directly add points to users bank or wallet'
usage = ".eco give <@USER> <wallet|bank> <AMMOUNT>"
permissions = "creator"

# directly add points to users bank or wallet
async def execute(bot, msg, path):
    
    args = msg.content[msg.content.find(' ')+1+len(name):].split()
    log.debug(args)

    if len(args) < 3:

        log.info('Bad args')
        await msg.reply(f"Usage: {usage}")
        return

    # args[0] should be "<!@USER.ID>"
    args[0] = bot.get_user(int(args[0][3:-1]))
    log.debug(f"args: {args[0]}")

    if args[0] is None:
        
        log.info("Bad args")
        await msg.reply(f"Usage: {usage}")
        return

    if args[1] not in ["wallet", "bank"]:
        
        log.info("Bad args")
        await msg.reply(f"Usage: {usage}")
        return

    try:
        args[2] = int(args[2])
 
    except ValueError:
        log.info("Bad args")
        await msg.reply(f"Usage: {usage}")
        return
 
    except:
        log.info("Unexpected Error")
        return

    userdata = eco_common.readFile(path, str(args[0].id))

    userdata[args[1]] += args[2]


    eco_common.writeFile(path, {str(args[0].id): userdata})
    log.info(f"Added {args[2]} points to {args[0].name}'s {args[1]}")
    await msg.reply(
        f"Gave {args[0].mention} {args[2]} points into their {args[1]}")