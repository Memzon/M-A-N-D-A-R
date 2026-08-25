import asyncio
import random
import logging

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.image_gen import generate_chest_image

log = logging.getLogger("EconoBot.Chest")


class ChestButton(discord.ui.Button):
    def __init__(self, index: int):
        super().__init__(
            label=f"Sandık {index + 1}",
            style=discord.ButtonStyle.secondary,
            emoji="🎁",
        )
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view: "ChestView" = self.view
        db = interaction.client.db

        if interaction.user.id in view.opened_users:
            await interaction.response.send_message(
                "Bu etkinlikte zaten bir sandık açtın! 😉", ephemeral=True
            )
            return

        if view.claimed_by.get(self.index) is not None:
            await interaction.response.send_message(
                "Bu sandık az önce başka biri tarafından açıldı, başka birini dene!",
                ephemeral=True,
            )
            return

        reward = view.rewards[self.index]
        view.claimed_by[self.index] = (interaction.user.id, reward)
        view.opened_users.add(interaction.user.id)

        db.add_balance(interaction.user.id, reward, chest=True)

        self.disabled = True
        self.label = f"{interaction.user.display_name} → {reward} {config.CURRENCY_EMOJI}"
        self.style = discord.ButtonStyle.success

        await interaction.response.edit_message(view=view)
        await interaction.followup.send(
            f"🎉 {interaction.user.mention} sandığı açtı ve **{reward} {config.CURRENCY_NAME}** kazandı!",
        )

        if len(view.opened_users) == len(view.rewards):
            for item in view.children:
                item.disabled = True
            await interaction.message.edit(view=view)


class ChestView(discord.ui.View):
    def __init__(self, rewards: list[int]):
        super().__init__(timeout=300)
        self.rewards = rewards
        self.claimed_by: dict[int, tuple[int, int] | None] = {i: None for i in range(len(rewards))}
        self.opened_users: set[int] = set()

        for i in range(len(rewards)):
            self.add_item(ChestButton(i))

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class ChestEvent(commands.Cog):
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
        channel = self.bot.get_channel(config.CHEST_CHANNEL_ID)
        if channel is None:
            log.warning("CHEST_CHANNEL_ID bulunamadı, sandık etkinliği devre dışı bırakıldı.")
            return

        while not self.bot.is_closed():
            wait_minutes = random.randint(config.CHEST_MIN_INTERVAL, config.CHEST_MAX_INTERVAL)
            await asyncio.sleep(wait_minutes * 60)
            try:
                await self._spawn_event(channel)
            except Exception:
                log.exception("Sandık etkinliği gönderilirken hata oluştu.")

    async def _spawn_event(self, channel: discord.TextChannel):
        rewards = [
            random.randint(config.CHEST_MIN_REWARD, config.CHEST_MAX_REWARD) for _ in range(5)
        ]
        image_buf = generate_chest_image(5)
        file = discord.File(image_buf, filename="sandik.png")

        embed = discord.Embed(
            title="💎 VIP Sandık Etkinliği Başladı!",
            description=(
                "Aşağıdaki **5 sandıktan** birini seç ve içindeki ödülü kap!\n"
                "Her sandık yalnızca bir kez açılabilir, her kullanıcı yalnızca bir sandık açabilir."
            ),
            color=discord.Color.gold(),
        )
        embed.set_image(url="attachment://sandik.png")
        embed.set_footer(text="En hızlı davranan en iyi ödülü kapabilir!")

        view = ChestView(rewards)

        await channel.send(embed=embed, file=file, view=view)

    @app_commands.command(name="sandik-baslat", description="[Admin] Sandık etkinliğini hemen başlatır.")
    @app_commands.checks.has_permissions(administrator=True)
    async def force_chest(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(config.CHEST_CHANNEL_ID) or interaction.channel
        await interaction.response.send_message("Sandık etkinliği başlatılıyor...", ephemeral=True)
        await self._spawn_event(channel)

    @force_chest.error
    async def force_chest_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "Bu komutu kullanmak için yönetici yetkin olması gerekiyor.", ephemeral=True
            )
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(ChestEvent(bot))
