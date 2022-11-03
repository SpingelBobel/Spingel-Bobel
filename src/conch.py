import datetime
import logging
import traceback

import discord
from discord.ext import commands

from src.manager import Manager
from src.utils.common import load_references


async def prefix(_bot, message):
    return commands.when_mentioned(_bot, message) + ['==']


logger = logging.getLogger(__name__)
logger.info("Starting \'Magic Conch\' bot script!")
conch_bot = commands.AutoShardedBot(
    command_prefix=prefix,
    intents=discord.Intents.default()
)
conch_bot.remove_command('help')
version = "v5.0.0r"
STARTED = False


@conch_bot.event
async def on_ready():
    global STARTED
    logger.info(f"Successfully logged into account {conch_bot.user.name} with id {str(conch_bot.user.id)} and version {version}")
    await conch_bot.change_presence(activity=discord.Game(name='the game of life!'))
    if not STARTED:
        conch_bot.started = datetime.datetime.now()
        conch_bot.version = version
        conch_bot.total_questions = 0

        await conch_bot.add_cog(Manager(conch_bot, "magicconch"))
        loaded, total = await conch_bot.get_cog("Manager").load_all_cogs()
        await conch_bot.get_channel(load_references()['admin_channel']).send(f"Magic Conch is online.\nLoaded {loaded} of {total} cogs.")

        STARTED = True


@conch_bot.event
async def on_error(event_method, *_, **__):
    logger.info(f"Catching exception in {event_method}")
    try:
        logger.info(''.join(traceback.format_exc()))
    except:
        logger.info("Unhandled error, could not print traceback")


@conch_bot.event
async def on_command_error(context, exception):
    ignored = (commands.CommandNotFound, commands.CheckFailure)
    if isinstance(exception, ignored):
        return
    
    exc = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    exc = ''.join(exc) if isinstance(exc, list) else exc
    logger.error(f'Ignoring exception in command {context.command}:\n{exc}')
