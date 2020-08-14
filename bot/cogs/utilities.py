import datetime
from asyncio import sleep
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
from discord.utils import sleep_until
from bot import settings


def convert_time(time, period):
    result = None
    try:
        time = int(time)
        if "sec" in period:
            result = time
        elif "min" in period:
            result = time * 60
        elif "hour" in period:
            result = time * (60**2)
    except ValueError:
        pass
    return result


class Utilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.index = 0

    async def reminder_wrapper(self, time, period, ctx, msg="Reminder!"):

        @tasks.loop(count=1)
        async def create_reminder():
            seconds = convert_time(time, period)
            if not seconds:
                msg = "Please enter a valid time and period (i.e .reminder 5 minutes)"
                await ctx.send(msg)
                return msg
            else:
                await sleep(seconds)
            return

        @create_reminder.after_loop
        async def after_create_reminder():
            await ctx.send(msg)

        create_reminder.start()

    @command()
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg

    @command()
    async def reminder(self, ctx, time, period="minutes"):
        await self.reminder_wrapper(ctx=ctx, time=time, period=period)
        return

    @command()
    async def drink(self, ctx):
        await ctx.send(f"{ctx.author.mention} I got you, mate.")
        base_msg = f"OY! {ctx.author.mention}, drink some water, mate."
        await self.reminder_wrapper(ctx=ctx, time=5, period="minutes", msg=base_msg)
        await self.reminder_wrapper(ctx=ctx, time=10, period="minutes", msg=base_msg + "\nYou can have another if you'd like.")


def setup(bot: Bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Utilities(bot))