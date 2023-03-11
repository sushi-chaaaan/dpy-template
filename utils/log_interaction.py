from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, Union, overload

from discord import Interaction, Member, Message, User

from const import app_command_log
from utils.logger import getMyLogger

# 第2引数以降をEllipsisにして任意にしたかったが無理らしい
AppCommandFunc = Union[
    Callable[[Interaction], Coroutine[Any, Any, None]],
    Callable[[Interaction, User], Coroutine[Any, Any, None]],
    Callable[[Interaction, Member], Coroutine[Any, Any, None]],
    Callable[[Interaction, Message], Coroutine[Any, Any, None]],
]


@overload
def log_interaction(func: Callable[[Interaction], Coroutine[Any, Any, None]]) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def log_interaction(
    func: Callable[[Interaction, User], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def log_interaction(
    func: Callable[[Interaction, Member], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


@overload
def log_interaction(
    func: Callable[[Interaction, Message], Coroutine[Any, Any, None]]
) -> Callable[..., Coroutine[Any, Any, None]]:
    ...


def log_interaction(func: AppCommandFunc):  # pyright: ignore
    @wraps(func)  # pyright: ignore
    async def decorator(*args, **kwargs):
        # write log
        if isinstance(args[0], Interaction):
            logger = getMyLogger(func.__name__)
            logger.debug(
                app_command_log(
                    interaction=args[0],
                )
            )

        return await func(*args, **kwargs)

    return decorator
