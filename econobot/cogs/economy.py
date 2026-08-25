import discord
from discord.ext import commands
from discord import app_commands

import config


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bakiye", description="Kendi veya başka birinin bakiyesini gösterir.")
    @app_commands.describe(kullanici="Bakiyesine bakmak istediğin kullanıcı (boş bırakılırsa sen).")
    async def balance(self, interaction: discord.Interaction, kullanici: discord.Member | None = None):
        target = kullanici or interaction.user
        bal = self.bot.db.get_balance(target.id)

        embed = discord.Embed(
            title="💰 VIP Cüzdan",
            description=f"{target.mention} adlı kullanıcının bakiyesi:",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Bakiye", value=f"**{bal:,} {config.CURRENCY_EMOJI} {config.CURRENCY_NAME}**")
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="liderlik", description="En zengin kullanıcıları gösterir.")
    async def leaderboard(self, interaction: discord.Interaction):
        rows = self.bot.db.leaderboard(10)
        if not rows:
            await interaction.response.send_message("Henüz kimsenin bakiyesi yok.")
            return

        lines = []
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, balance) in enumerate(rows):
            prefix = medals[i] if i < 3 else f"{i + 1}."
            lines.append(f"{prefix} <@{user_id}> — **{balance:,} {config.CURRENCY_EMOJI}**")

        embed = discord.Embed(
            title="🏆 VIP Liderlik Tablosu",
            description="\n".join(lines),
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="istatistik", description="Sandık ve hız etkinliği istatistiklerini gösterir.")
    @app_commands.describe(kullanici="İstatistiklerine bakmak istediğin kullanıcı (boş bırakılırsa sen).")
    async def stats(self, interaction: discord.Interaction, kullanici: discord.Member | None = None):
        target = kullanici or interaction.user
        balance, chests, wins, total_earned = self.bot.db.stats(target.id)

        embed = discord.Embed(title=f"📊 {target.display_name} İstatistikleri", color=discord.Color.teal())
        embed.add_field(name="Bakiye", value=f"{balance:,} {config.CURRENCY_EMOJI}")
        embed.add_field(name="Açılan Sandık", value=str(chests))
        embed.add_field(name="El Alıştırması Galibiyeti", value=str(wins))
        embed.add_field(name="Toplam Kazanç", value=f"{total_earned:,} {config.CURRENCY_EMOJI}")
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coin-ver", description="[Admin] Bir kullanıcıya coin verir.")
    @app_commands.checks.has_permissions(administrator=True)
    async def give_coin(self, interaction: discord.Interaction, kullanici: discord.Member, miktar: int):
        if miktar <= 0:
            await interaction.response.send_message("Miktar pozitif olmalı.", ephemeral=True)
            return
        self.bot.db.add_balance(kullanici.id, miktar)
        await interaction.response.send_message(
            f"✅ {kullanici.mention} kullanıcısına **{miktar:,} {config.CURRENCY_EMOJI}** eklendi."
        )

    @app_commands.command(name="coin-al", description="[Admin] Bir kullanıcıdan coin alır.")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_coin(self, interaction: discord.Interaction, kullanici: discord.Member, miktar: int):
        if miktar <= 0:
            await interaction.response.send_message("Miktar pozitif olmalı.", ephemeral=True)
            return
        current = self.bot.db.get_balance(kullanici.id)
        self.bot.db.set_balance(kullanici.id, max(0, current - miktar))
        await interaction.response.send_message(
            f"✅ {kullanici.mention} kullanıcısından **{miktar:,} {config.CURRENCY_EMOJI}** alındı."
        )

    @give_coin.error
    @remove_coin.error
    async def admin_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "Bu komutu kullanmak için yönetici yetkin olması gerekiyor.", ephemeral=True
            )
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
