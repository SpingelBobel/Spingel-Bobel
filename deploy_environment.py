import asyncio
import sys

from src.utils import logger
from src.utils import common
from src import spingel as spingel_bot

DEBUG_MODE = not (len(sys.argv) == 2 and sys.argv[1] == "prod")

loop = asyncio.get_event_loop()
conch = loop.create_task(conch_bot.conch_bot.start(common.load_creds(DEBUG_MODE, common.EcosystemBots.SpingelBobel)))
gathered = asyncio.gather(bobel, loop=loop)
loop.run_until_complete(gathered)
