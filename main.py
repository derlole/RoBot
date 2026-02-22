import discord
from discord.ext import commands
import os
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

async def setup_hook(self):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await self.load_extension(f"cogs.{filename[:-3]}")

    print("Cogs geladen!")

    await self.tree.sync()
bot = MyBot()

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

bot.run(TOKEN)