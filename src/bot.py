import asyncio
import json
import os
from typing import TYPE_CHECKING, Any

import discord

# import sentry_sdk
from discord.ext import commands

from const import COMMAND_LOG_FORMAT
from utils.logger import getMyLogger

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()

if TYPE_CHECKING:
    import logging


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # self.init_sentry()
        self.config = self.load_config()
        self.logger = self.get_logger()

        # set to None if you want to sync as global commands
        self.app_cmd_sync_target = discord.Object(int(os.environ["GUILD_ID"]))

        # set intents
        intents = discord.Intents.all()
        intents.typing = False

        super().__init__(
            command_prefix=self.config.get("prefix", "!"),
            intents=intents,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        await self.set_pre_invoke_hook()
        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self) -> None:
        self.print_status()

    async def load_exts(self) -> None:
        ext_paths = self.config.get("cogs", None)
        if ext_paths is None:
            return

        for ext in ext_paths:
            try:
                await self.load_extension(ext)
            except Exception as e:
                self.logger.exception(f"Failed to load {ext}", exc_info=e)
        return

    async def sync_app_commands(self) -> None:
        try:
            await self.tree.sync(guild=self.app_cmd_sync_target)
        except Exception as e:
            self.logger.exception("Failed to sync application commands", exc_info=e)
        else:
            self.logger.info("Application commands synced successfully")

    async def setup_views(self) -> None:
        pass

    def load_config(self) -> dict[str, Any]:
        with open("config.json", "r") as f:
            return json.load(f)

    def get_logger(self) -> logging.Logger:
        logger = getMyLogger(__name__)
        try:
            self.logger.setLevel(self.config.get("log_level", "INFO"))
        except (TypeError, ValueError):
            self.logger.setLevel("INFO")
        return logger

    async def set_pre_invoke_hook(self):
        @self.before_invoke
        async def write_debug_log(ctx: commands.Context) -> None:  # type: ignore
            self.logger.debug(
                COMMAND_LOG_FORMAT.format(
                    command_name=ctx.command.name if ctx.command else "None",
                    guild_id=ctx.guild.id if ctx.guild else "None",
                    channel_id=ctx.channel.id,
                    author_id=ctx.author.id,
                    author_name=ctx.author.name,
                )
            )

    def print_status(self) -> None:
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")  # type: ignore
        self.logger.info(f"Connected to {len(self.guilds)} guilds")  # pyright: ignore
        self.logger.info("Bot is ready")

    # def init_sentry(self) -> None:
    #     sentry_sdk.init(
    #         dsn=os.environ["SENTRY_DSN"],
    #         # Set traces_sample_rate to 1.0 to capture 100%
    #         # of transactions for performance monitoring.
    #         # We recommend adjusting this value in production.
    #         traces_sample_rate=1.0,
    #     )

    def runner(self) -> None:
        try:
            asyncio.run(self._runner())
        except Exception as e:
            self.logger.critical("SystemExit Detected, shutting down...", exc_info=e)
            asyncio.run(self.shutdown(status=1))
            return

    async def _runner(self) -> None:
        async with self:
            await self.start(os.environ["DISCORD_BOT_TOKEN"])

    async def shutdown(self, status: int = 0) -> None:
        import sys

        # from sentry_sdk import Hub
        # # shutdown Sentry
        # client = Hub.current.client
        # if client is not None:
        #     client.close(timeout=2.0)

        self.logger.info("Shutting down...")
        await self.close()
        sys.exit(status)
