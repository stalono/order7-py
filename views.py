import discord
from discord import Interaction


class RefreshView(discord.ui.View):
    def __init__(self, dynamic_embed):
        super().__init__()
        self.value = None
        self.dynamic_embed = dynamic_embed

    @discord.ui.button(label='Обновить', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.dynamic_embed(), view=self)

class EmbedBuilderModal(discord.ui.Modal):
    def __init__(self, interaction_to_reply: Interaction):
        super().__init__(title="Создание Embed", custom_id="embedBuilder")
        self.interaction_to_reply = interaction_to_reply

    titleInput = discord.ui.TextInput(label="Заголовок", min_length=1, max_length=256, custom_id="titleInput", style=discord.enums.TextStyle.short, required=False)
    descriptionInput = discord.ui.TextInput(label="Описание", min_length=1, max_length=2048, custom_id="descriptionInput", style=discord.enums.TextStyle.paragraph, required=False)
    colorInput = discord.ui.TextInput(label="Цвет в формате #ffffff", min_length=1, max_length=7, custom_id="colorInput", style=discord.enums.TextStyle.short, required=False)
    imageInput = discord.ui.TextInput(label="Ссылка на изображение", min_length=1, max_length=2048, custom_id="imageInput", style=discord.enums.TextStyle.short, required=False)
    thumbnailInput = discord.ui.TextInput(label="Ссылка на миниатюру", min_length=1, max_length=2048, custom_id="thumbnailInput", style=discord.enums.TextStyle.short, required=False)

    async def on_submit(self, interaction: Interaction):
        embed = discord.Embed()
        if self.colorInput.value:
            try:
                color = int(self.colorInput.value[1:], 16)
            except ValueError:
                await interaction.response.send_message(embed=error_embed("Вы ввели неверный цветовой код, его формат должен быть #ffffff"), ephemeral=True)
                return
            embed.colour = color
        if self.titleInput.value:
            embed.title = self.titleInput.value
        if self.descriptionInput.value:
            embed.description = self.descriptionInput.value
        if self.imageInput.value:
            embed.set_image(url=self.imageInput.value)
        if self.thumbnailInput.value:
            embed.set_thumbnail(url=self.thumbnailInput.value)
        await interaction.response.send_message(embed=embed)

    async def on_timeout(self):
        await self.interaction_to_reply.response.send_message(embed=error_embed("Время на заполнение формы вышло :("), ephemeral=True)

    async def on_error(self, interaction: Interaction, error: Exception):
        await self.interaction_to_reply.response.send_message(embed=error_embed("Произошла ошибка при заполнении формы :(", error), ephemeral=True)

def error_embed(message: str, error: Exception = None) -> discord.Embed:
    embed = discord.Embed(title=f"Ошибка: {message}", color=discord.Color.red())
    if error:
        embed.description(f"```py\n{error}```")
    return embed

def success_embed(message: str) -> discord.Embed:
    return discord.Embed(title=message, color=discord.Color.green())

def profile_embed(user: discord.User, userData: any) -> discord.Embed:
    embed = discord.Embed(
        title=f"Профиль — {user.name}#{user.discriminator}",
        description=f"**> Баланс:**```{userData['balance']}```\n"
        f"> **Голосовой онлайн:**\n```{userData['voice']}```\n"
        f"> **Голосовой онлайн за сегодня:**\n```{userData['voiceToday']}```\n",
        color=discord.Color.from_str("#2f3136")
    )
    return embed