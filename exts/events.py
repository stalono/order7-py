import discord
from discord.ext import commands, tasks
import time


async def setup(client: commands.Bot):
    Database = client.Database.Users

    @tasks.loop(seconds=5)
    async def loop(member: discord.Member):
        userData = await Database.find(str(member.id))
        daysSince = int(time.time() / 86400)
        if daysSince != userData["voiceLastDay"]:
            await Database.set(str(member.id), {"voiceLastDay": daysSince, "voiceToday": 1})
        else:
            await Database.increase(str(member.id), {"voiceToday": 1})
        await Database.increase(str(member.id), {"voice": 1, "balance": 2})

    @client.event
    async def on_ready():
        print("Ready!")
        client.start_time = time.time()

    @client.event
    async def on_voice_state_update(member: any, before: any, after: any):
        if before.channel is None and after.channel is not None:
            loop.start(member)

        elif before.channel is not None and after.channel is None:
            await Database.increase(str(member.id), {"voice": -1})
            loop.stop()
