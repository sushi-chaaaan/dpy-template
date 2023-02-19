from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    # import some original class
    pass


class SomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog((SomeCog(bot)))
