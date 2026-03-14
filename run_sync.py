import discord
from discord.ext import commands
import asyncio
import os
from config import TOKEN

intents = discord.Intents.all()

class SyncBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # load cogs so commands are registered in tree
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py') and not filename.startswith('_'):
                await self.load_extension(f"cogs.{filename[:-3]}")

        print('Bot user id (will be available after ready):', self.user)
        print('Application id (may be None until ready):', self.application_id)
        try:
            print('Starte globale Sync...')
            await self.tree.sync()
            print('Sync beendet. Globale Commands können bis zu 1 Stunde dauern, bis sie verfügbar sind.')
        except Exception as e:
            print('Fehler beim Sync:', e)

        try:
            cmds = await self.tree.fetch_commands()
            print('Registrierte globale Commands nach Sync:')
            for c in cmds:
                print(' -', c.name)
        except Exception as e:
            print('Fehler beim Abrufen der globalen Commands nach Sync:', e)

        await self.close()


bot = SyncBot()

if __name__ == '__main__':
    bot.run(TOKEN)
