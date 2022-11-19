import discord
from discord import app_commands
from discord.ext import commands
from views import RefreshView, EmbedBuilderModal
from time import time

class PingCommand(app_commands.Command):
    def __init__(self, client: commands.Bot):
        super().__init__(name="ping", description="Время отклика бота", callback=self.callback)
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.dynamicPingEmbed(), view=RefreshView(self.dynamicPingEmbed))

    def dynamicPingEmbed(self):
        latency = round(self.client.latency * 1000)
        if latency > 100:
            color = discord.Color.red()
        else:
            color = discord.Color.green()
        pingEmbed = discord.Embed(
            title = f"Пинг бота: {latency} мс",
            color = color
        )
        
        return pingEmbed

class UptimeCommand(app_commands.Command):
    def __init__(self, client: commands.Bot):
        super().__init__(name="uptime", description="Время работы бота", callback=self.callback)
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.dynamicUptimeEmbed(), view=RefreshView(self.dynamicUptimeEmbed))

    def dynamicUptimeEmbed(self):
        uptimeMS = time() - self.client.start_time
        uptime = str(int(uptimeMS // 86400)) + " дней " + str(int(uptimeMS % 86400 // 3600)) + " часов " + str(int(uptimeMS % 3600 // 60)) + " минут " + str(int(uptimeMS % 60)) + " секунд"
        uptimeEmbed = discord.Embed(
            title = f"Бот работает уже: {uptime}",
            color = discord.Color.green()
        )
        
        return uptimeEmbed

class SayCommand(app_commands.Command):
    def __init__(self, client: commands.Bot):
        super().__init__(name="say", description="Повторяет сообщение", callback=self.callback)
        self.client = client

    @app_commands.describe(text="Текст сообщения")
    async def callback(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text)

class EmbedCommand(app_commands.Command):
    def __init__(self, client: commands.Bot):
        super().__init__(name="embed", description="Отправляет в чат эмбед", callback=self.callback)
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EmbedBuilderModal(interaction))

async def setup(client: commands.Bot):
    client.tree.add_command(PingCommand(client))
    client.tree.add_command(UptimeCommand(client))
    client.tree.add_command(SayCommand(client))
    client.tree.add_command(EmbedCommand(client))