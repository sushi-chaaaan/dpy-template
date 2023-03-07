import discord
from discord.ext import commands

from utils.logger import getMyLogger

INTERACTION_LOG_FORMAT = """
[Interaction Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""

COMMAND_LOG_FORMAT = """
[Ext Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""


def command_log(context: discord.Interaction | commands.Context):  # type: ignore
    # ここに引数情報のジェネリクスなどをつけてなんとかする
    def _command_log(func):
        async def wrapper(*args, **kwargs):
            # write log
            logger = getMyLogger(__name__)

            if isinstance(context, discord.Interaction):
                if context.command is not None:
                    logger.info(
                        INTERACTION_LOG_FORMAT.format(
                            command_name=context.command.name if context.command is not None else "None",
                            guild_id=context.guild.id if context.guild is not None else "None",
                            channel_id=context.channel.id if context.channel is not None else "None",
                            author_id=context.user.id,
                            author_name=context.user.name,
                        )
                    )

            elif isinstance(context, commands.Context):
                if context.command is not None:
                    logger.info(
                        COMMAND_LOG_FORMAT.format(
                            command_name=context.command.name if context.command is not None else "None",
                            guild_id=context.guild.id if context.guild is not None else "None",
                            channel_id=context.channel.id if context.channel is not None else "None",
                            author_id=context.author.id,
                            author_name=context.author.name,
                        )
                    )

            else:
                pass
            return await func(*args, **kwargs)

        return wrapper

    return _command_log
