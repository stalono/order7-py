import time
import discord
from discord import app_commands, User
from discord.ext import commands
from views import profile_embed

class ProfileCommand(app_commands.Command):
    def __init__(self, client: commands.Bot):
        super().__init__(name="profile", description="Получить информацию о пользователе", callback=self.callback)
        self.client = client

    @app_commands.describe(user="Пользователь")
    async def callback(self, interaction: discord.Interaction, user: User = None):
        if user is None:
            user = interaction.user
        
        Database = self.client.Database.Users
        userData = await Database.find(str(user.id))
        daysSince = int(time.time() / 86400)
        if daysSince != userData["voiceLastDay"]:
            await Database.set(str(user.id), {"voiceLastDay": daysSince, "voiceToday": 0})
        await interaction.response.send_message(embed=profile_embed(user, userData))
        

async def setup(client: commands.Bot):
    client.tree.add_command(ProfileCommand(client))