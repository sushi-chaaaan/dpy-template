from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, overload

from discord import Interaction
from discord.ext.commands import Context

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


@overload
def command_log(func: Callable[[Context], Coroutine[Any, Any, None]]):  # type: ignore
    ...


@overload
def command_log(func: Callable[[Interaction], Coroutine[Any, Any, None]]):
    ...


def command_log(func: Callable[[Interaction | Context, Any | None], Coroutine[Any, Any, None]]):  # type:ignore
    # ここに引数情報のジェネリクスなどをつけてなんとかする
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        # write log
        logger = getMyLogger("command")
        logger.info("command log")
        return await func(*args, **kwargs)

    return _wrapper


@command_log
async def interaction_log(interaction: Interaction):
    return
