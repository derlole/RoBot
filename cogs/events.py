from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.name} ist dem Server beigetreten!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if "hello" in message.content.lower():
            await message.channel.send("Hi!")

async def setup(bot):
    await bot.add_cog(Events(bot))