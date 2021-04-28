import os
import traceback
import logging

from discord.ext import commands

from src.utils import checks


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Loaded Manager Cog")
        self.load_all_cogs()

    @staticmethod
    def get_all_cogs():
        return [f[:-3] for f in os.listdir("src/cogs/") if f.endswith('.py')]

    def load_all_cogs(self):
        loaded = 0
        cogs = self.get_all_cogs()
        for cog in cogs:
            if self.load_cog(cog):
                loaded += 1
        return loaded, len(cogs)

    def unload_all_cogs(self):
        unloaded = 0
        cogs = self.get_all_cogs()
        for cog in cogs:
            if self.unload_cog(cog):
                unloaded += 1
        return unloaded, len(cogs)

    def load_cog(self, cog_name):
        try:
            self.logger.info(f"attempting to load cog {cog_name}")
            self.bot.load_extension(f"src.cogs.{cog_name}")
        except Exception as ex:
            self.logger.info("could not initialize")
            self.logger.info(''.join(traceback.format_exception(type(ex), ex, ex.__traceback__)))
            return False
        return True

    def unload_cog(self, cog_name):
        try:
            self.logger.info(f"attempting to unload cog {cog_name}")
            self.bot.unload_extension(f"src.cogs.{cog_name}")
        except Exception as ex:
            self.logger.info("could not initialize")
            self.logger.info(''.join(traceback.format_exception(type(ex), ex, ex.__traceback__)))
            return False
        return True

    def reload_cog(self, cog_name):
        self.unload_cog(cog_name)
        return self.load_cog(cog_name)

    @commands.command()
    @checks.admin()
    async def loadall(self, ctx):
        self.logger.info(f"{ctx.author.id} `loadall` invoked by '{ctx.author.name}'")
        unloaded, total = self.load_all_cogs()
        await ctx.channel.send(f"`{unloaded} of {total}` loaded")

    @commands.command()
    @checks.admin()
    async def unloadall(self, ctx):
        self.logger.info(f"{ctx.author.id} `unloadall` invoked by '{ctx.author.name}'")
        unloaded, total = self.unload_all_cogs()
        await ctx.channel.send(f"`{unloaded} of {total}` unloaded")

    @commands.command()
    @checks.admin()
    async def load(self, ctx, cog_name: str=''):
        self.logger.info(f"{ctx.author.id} `load` invoked by '{ctx.author.name}' [{cog_name}]")
        if cog_name not in self.get_all_cogs():
            await ctx.channel.send(f"Could not find cog `{cog_name}`")
        elif self.load_cog(cog_name):
            await ctx.channel.send(f"`{cog_name}` loaded")
        else:
            await ctx.channel.send(f"`{cog_name}` was not loaded. Check logs.")

    @commands.command()
    @checks.admin()
    async def unload(self, ctx, cog_name: str=''):
        self.logger.info(f"{ctx.author.id} `unload` invoked by '{ctx.author.name}' [{cog_name}]")
        if cog_name not in self.get_all_cogs():
            await ctx.channel.send(f"Could not find cog `{cog_name}`")
        elif self.unload_cog(cog_name):
            await ctx.channel.send(f"`{cog_name}` unloaded")
        else:
            await ctx.channel.send(f"`{cog_name}` was not unloaded. Check logs.")

    @commands.command()
    @checks.admin()
    async def reload(self, ctx, cog_name: str=''):
        self.logger.info(f"{ctx.author.id} `reload` invoked by '{ctx.author.name}' [{cog_name}]")
        if cog_name not in self.get_all_cogs():
            await ctx.channel.send(f"Could not find cog `{cog_name}`")
        elif self.reload_cog(cog_name):
            await ctx.channel.send(f"`{cog_name}` reloaded")
        else:
            await ctx.channel.send(f"`{cog_name}` was not reloaded. Check logs.")

    @commands.command()
    @checks.admin()
    async def cogs(self, ctx, cog_name: str=''):
        self.logger.info(f"{ctx.author.id} `cogs` invoked by '{ctx.author.name}' [{cog_name}]")
        cogs = "  " + '\n  '.join(self.get_all_cogs()) + "  "
        await ctx.channel.send(f"```src/cogs/\n{cogs}\n```")


def setup(bot):
    bot.add_cog(Manager(bot))
