import asyncio
import random
import string
import logging

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.image_gen import generate_speed_image

log = logging.getLogger("EconoBot.Speed")


def _generate_code(length: int) -> str:
    # Karıştırılabilecek karakterleri (O/0, I/1) çıkararak okunabilirliği artırıyoruz
    alphabet = "".join(c for c in string.ascii_uppercase if c not in "OI") + "23456789"
    return "".join(random.choice(alphabet) for _ in range(length))


class SpeedEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.task: asyncio.Task | None = None

    async def cog_load(self):
        self.task = self.bot.loop.create_task(self._loop())

    async def cog_unload(self):
        if self.task:
            self.task.cancel()

    async def _loop(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(config.SPEED_CHANNEL_ID)
        if channel is None:
            log.warning("SPEED_CHANNEL_ID bulunamadı, el alıştırması etkinliği devre dışı bırakıldı.")
            return

        while not self.bot.is_closed():
            wait_minutes = random.randint(config.SPEED_MIN_INTERVAL, config.SPEED_MAX_INTERVAL)
            await asyncio.sleep(wait_minutes * 60)
            try:
                await self._spawn_event(channel)
            except Exception:
                log.exception("El alıştırması etkinliği sırasında hata oluştu.")

    async def _spawn_event(self, channel: discord.TextChannel):
        code = _generate_code(config.SPEED_CODE_LENGTH)
        reward = random.randint(config.SPEED_MIN_REWARD, config.SPEED_MAX_REWARD)

        image_buf = generate_speed_image(code)
        file = discord.File(image_buf, filename="hiz.png")

        embed = discord.Embed(
            title="⚡ El Alıştırması Zamanı!",
            description=(
                f"Görseldeki kodu **birebir aynı şekilde** ilk yazan kişi "
                f"**{reward} {config.CURRENCY_NAME}** {config.CURRENCY_EMOJI} kazanır!\n"
                f"Süre: **{config.SPEED_TIMEOUT} saniye**"
            ),
            color=discord.Color.blue(),
        )
        embed.set_image(url="attachment://hiz.png")

        await channel.send(embed=embed, file=file)

        def check(m: discord.Message):
            return (
                m.channel.id == channel.id
                and not m.author.bot
                and m.content.strip().upper() == code
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=config.SPEED_TIMEOUT)
        except asyncio.TimeoutError:
            await channel.send(f"⌛ Süre doldu! Kodu doğru yazan olmadı. Doğru kod: **{code}**")
        else:
            self.bot.db.add_balance(msg.author.id, reward, speed=True)
            await channel.send(
                f"🏆 {msg.author.mention} kodu ilk doğru yazan oldu ve "
                f"**{reward} {config.CURRENCY_NAME}** {config.CURRENCY_EMOJI} kazandı!"
            )

    @app_commands.command(name="hiz-baslat", description="[Admin] El alıştırması etkinliğini hemen başlatır.")
    @app_commands.checks.has_permissions(administrator=True)
    async def force_speed(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(config.SPEED_CHANNEL_ID) or interaction.channel
        await interaction.response.send_message("El alıştırması etkinliği başlatılıyor...", ephemeral=True)
        await self._spawn_event(channel)

    @force_speed.error
    async def force_speed_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "Bu komutu kullanmak için yönetici yetkin olması gerekiyor.", ephemeral=True
            )
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(SpeedEvent(bot))
