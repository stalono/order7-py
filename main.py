import asyncio
import logging
import logging.handlers
import sys

from typing import List, Optional
from mongo import Database

import discord
from discord.ext import commands
from configparser import ConfigParser


class Client(commands.Bot):
    def __init__(
        self,
        *args,
        config: List[str],
        initial_extensions: List[str],
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.Database = None
        self.config = config
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        self.Database = await Database.connect()
        for extension in self.initial_extensions:
            if extension in self.extensions:
                await self.reload_extension(extension)
            else:
                await self.load_extension(extension)
        if len(sys.argv) > 1 and self.testing_guild_id:
            if sys.argv[1] == "--sync":
                guild = discord.Object(self.testing_guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                print("Synced commands to testing guild.")
            if sys.argv[1] == "--unsyncall":
                guild = discord.Object(self.testing_guild_id)
                self.tree.clear_commands(guild=None)
                await self.tree.sync()
                print("Unsynced all commands.")
            await self.close()
            return

async def main():

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    config = ConfigParser()
    config.read('config.ini')

    exts = [ext.strip() for ext in config.get('BOT', 'exts').split(',')]

    intents = discord.Intents.default()
    intents.voice_states = True

    async with Client(commands.when_mentioned, intents=intents, initial_extensions=exts, testing_guild_id=958262046745587733, config=config) as client:

        await client.start(config.get('BOT', 'token'))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass