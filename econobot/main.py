import asyncio
import logging
import os

import discord
from discord.ext import commands

import config
from utils.db import Database

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("EconoBot")

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True


class EconoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=INTENTS, help_command=None)
        db_path = os.path.join(os.path.dirname(__file__), "data", "economy.db")
        self.db = Database(db_path)

    async def setup_hook(self):
        for ext in ("cogs.economy", "cogs.chest_event", "cogs.speed_event"):
            await self.load_extension(ext)
            log.info(f"Yüklendi: {ext}")

        if config.GUILD_ID:
            guild = discord.Object(id=config.GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info("Komutlar sunucuya senkronize edildi (anında görünür).")
        else:
            await self.tree.sync()
            log.info("Komutlar global senkronize edildi (Discord'da yayılması saatler sürebilir).")

    async def on_ready(self):
        log.info(f"{self.user} olarak giriş yapıldı. (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="💎 VIP Ekonomi")
        )


async def main():
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    bot = EconoBot()
    async with bot:
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    if not config.TOKEN:
        raise SystemExit("HATA: .env dosyasında DISCORD_TOKEN tanımlı değil!")
    asyncio.run(main())
