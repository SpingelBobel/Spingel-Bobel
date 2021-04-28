from discord.ext import commands


def _is_dove(user):
    return user.id == 304695409031512064


def admin():
    async def pred(ctx):
        return _is_dove(ctx.author)
    return commands.check(pred)
