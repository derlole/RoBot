import discord
from discord.ext import commands
import os
from config import TOKEN

TEST_GUILD_ID = 1080867857652527184

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
        guild  = discord.Object(id=TEST_GUILD_ID)
        try:
            await self.tree.sync(guild=guild)
            print("Guild Commands synchronisiert!")
        except Exception as e:
            print("Fehler beim Synchronisieren der Guild-Commands:", e)
            print("Hinweis: Falls der Fehler 'Can not decode content-encoding: br' auftritt, installiere 'brotlicffi' oder 'brotli' in deiner venv (pip install brotlicffi).")

        # Debug: fetch and print registered guild commands to verify registration
        try:
            cmds = await self.tree.fetch_commands(guild=guild)
            print("Registrierte Guild-Commands:")
            for c in cmds:
                print(f" - {c.name} (id={getattr(c, 'id', 'n/a')})")
        except Exception as e:
            print("Fehler beim Abrufen der Guild-Commands:", e)
        # Zusätzlich: print global registrierte Commands und lokale Tree-Commands
        try:
            global_cmds = await self.tree.fetch_commands()
            print("Registrierte Global-Commands:")
            for c in global_cmds:
                print(f" - {c.name} (id={getattr(c, 'id', 'n/a')})")
        except Exception as e:
            print("Fehler beim Abrufen der Global-Commands:", e)

        print("Lokale Tree-Commands (im Speicher):")
        for c in self.tree.get_commands():
            print(f" - {c.name} (type={type(c)})")


bot = MyBot()

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

bot.run(TOKEN)