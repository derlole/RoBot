from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def echo(self, ctx, *, message: str):
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(General(bot))