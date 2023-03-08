from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, Union, overload

from discord import Interaction, Member, Message, User

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


# 第2引数以降をEllipsisにして任意にしたかったが無理らしい
AppCommandFunc = Union[
    Callable[[Interaction], Coroutine[Any, Any, None]],
    Callable[[Interaction, User], Coroutine[Any, Any, None]],
    Callable[[Interaction, Member], Coroutine[Any, Any, None]],
    Callable[[Interaction, Message], Coroutine[Any, Any, None]],
]


@overload
def before_interaction(func: Callable[[Interaction], Coroutine[Any, Any, None]]) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def before_interaction(
    func: Callable[[Interaction, User], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def before_interaction(
    func: Callable[[Interaction, Member], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def before_interaction(
    func: Callable[[Interaction, Message], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


# TODO: 任意の処理を受け取る
# https://zenn.dev/ryo_kawamata/articles/learn_decorator_in_python#%E5%BC%95%E6%95%B0%E3%82%92%E5%8F%97%E3%81%91%E5%8F%96%E3%82%8B%E9%96%A2%E6%95%B0%E3%83%87%E3%82%B3%E3%83%AC%E3%83%BC%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90
def before_interaction(func: AppCommandFunc):
    @wraps(func)
    async def decorator(*args, **kwargs):
        # write log
        if isinstance(args[0], Interaction):
            logger = getMyLogger(func.__name__)
            logger.debug(
                INTERACTION_LOG_FORMAT.format(
                    command_name=args[0].command.name if args[0].command else "None",
                    guild_id=args[0].guild_id,
                    channel_id=args[0].channel_id,
                    author_id=args[0].user.id,
                    author_name=args[0].user.name,
                )
            )

        return await func(*args, **kwargs)

    return decorator
