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
logger.info("Starting \'Spingel Bobel\' bot script!")
spingel_bot = commands.AutoShardedBot(
    command_prefix=prefix,
    intents=discord.Intents.default()
)
spingel_bot.remove_command('help')
version = "v5.0.0r"
STARTED = False


@spingel_bot.event
async def on_ready():
    global STARTED
    logger.info(f"Successfully logged into account {spingel_bot.user.name} with id {str(spingel_bot.user.id)} and version {version}")
    await spingel_bot.change_presence(activity=discord.Game(name='Playing With Batrick!'))
    if not STARTED:
        spingel_bot.started = datetime.datetime.now()
        spingel_bot.version = version
        spingel_bot.total_questions = 0

        await spingel_bot.add_cog(Manager(spingel_bot, "SpingelBobel"))
        loaded, total = await Spingel_bot.get_cog("Manager").load_all_cogs()
        await spingel_bot.tree.sync()
        await spingel_bot.get_channel(load_references()['admin_channel']).send(f"Spingel Bobel is online.\nLoaded {loaded} of {total} cogs.")

        STARTED = True


@spingel_bot.event
async def on_error(event_method, *_, **__):
    logger.info(f"Catching exception in {event_method}")
    try:
        logger.info(''.join(traceback.format_exc()))
    except:
        logger.info("Unhandled error, could not print traceback")


@spingel_bot.event
async def on_command_error(context, exception):
    ignored = (commands.CommandNotFound, commands.CheckFailure)
    if isinstance(exception, ignored):
        return
    
    exc = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    exc = ''.join(exc) if isinstance(exc, list) else exc
    logger.error(f'Ignoring exception in command {context.command}:\n{exc}')
