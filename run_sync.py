import discord
from discord.ext import commands
import asyncio
import os
from config import TOKEN

TEST_GUILD_ID = 1080867857652527184

intents = discord.Intents.all()

class SyncBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # load cogs so commands are registered in tree
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py') and not filename.startswith('_'):
                await self.load_extension(f"cogs.{filename[:-3]}")

        guild = discord.Object(id=TEST_GUILD_ID)
        print('Bot user id (will be available after ready):', self.user)
        print('Application id (may be None until ready):', self.application_id)
        try:
            print('Starte Guild sync...')
            await self.tree.sync(guild=guild)
            print('Sync beendet.')
        except Exception as e:
            print('Fehler beim Sync:', e)

        try:
            cmds = await self.tree.fetch_commands(guild=guild)
            print('Registrierte Guild-Commands nach Sync:')
            for c in cmds:
                print(' -', c.name)
        except Exception as e:
            print('Fehler beim Abrufen der Guild-Commands nach Sync:', e)

        await self.close()


bot = SyncBot()

if __name__ == '__main__':
    bot.run(TOKEN)
