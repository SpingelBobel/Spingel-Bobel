import datetime
import discord

from discord.ext import commands

from src.utils.async_base_cog import AsyncBaseCog


class Info(AsyncBaseCog):

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in [f'<@{self.bot.user.id}>', f'<@!{self.bot.user.id}>']:
            await self.send_help(message.channel, message.author)

    @commands.command(pass_context=True, aliases=['info', 'stat', 'stats', 'invite'])
    async def help(self, ctx):
        self.logger.info(f"{ctx.author.id} `help` invoked with by '{ctx.message.author.name}'")
        await self.send_help(ctx.channel, ctx.author)

    async def send_help(self, channel, user):
        time_diff = (datetime.datetime.now() - self.bot.started).total_seconds()
        time_days = divmod(time_diff, 86400)
        time_hours = divmod(time_days[1], 3600)
        time_minutes = divmod(time_hours[1], 60)
        time_seconds = divmod(time_minutes[1], 1)

        total_guilds = len(self.bot.guilds)
        total_questions = self.bot.total_questions

        embed = discord.Embed(
                title="Spingel Bobel Help, Info, and Statistics",
                description=
                f"**Commands and Usage**\n"
                f"<@{self.bot.user.id}> help, info, stat, stats, or invite: *this menu*\n"
                f"<@{self.bot.user.id}> [question]? : *asks the bot a question and requests a .png response*\n"
                f"\nThe following are my current session metrics and statistics!\n",
                color=self.bot.user.color
        ).set_thumbnail(
            url=self.bot.user.avatar.url
        ).set_footer(
            text=f"Requestor: {user.id}"
        ).add_field(
            name="Invite Link", inline=True,
            value="[Clicky](https://discord.com/oauth2/authorize?client_id=481916394410344450&scope=bot)"
        ).add_field(
            name="Support Server", inline=True,
            value="[Bikini Bottom](https://discord.gg/spongebob)"
        ).add_field(
            name="Version", inline=False,
            value=self.bot.version
        ).add_field(
            name="Uptime", inline=True,
            value=f"{int(time_days[0]):,}d, {int(time_hours[0]):,}h, {int(time_minutes[0]):,}m, and {int(time_seconds[0]):,}s"
        ).add_field(
            name="ALOC", inline=True,
            value=f"{556:,} lines"
        ).add_field(
            name="Guilds", inline=True,
            value=f"{total_guilds:,} servers"
        ).add_field(
            name="Shards", inline=True,
            value=f"{self.bot.shard_count:,} shards"
        ).add_field(
            name="All Time Questions", inline=True,
            value=f"{total_questions:,} responses so far..."
        )
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
