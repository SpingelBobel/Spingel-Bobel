from discord.ext import commands


def _is_dove(user):
    return user.id == 1171203015496175677

def admin():
    async def pred(ctx):
        return _is_dove(ctx.author)
   
    return commands.check(pred)
