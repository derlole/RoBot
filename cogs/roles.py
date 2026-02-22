import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listRoles")
    async def list_roles(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Dieser Command funktioniert nur in einem Server.")
            return

        member = ctx.author
        guild = ctx.guild
        user_roles = [role.name for role in member.roles if role.name != "@everyone"]

        all_roles = [role.name for role in guild.roles if role.name != "@everyone"]

        user_roles_text = ", ".join(user_roles) if user_roles else "Keine Rollen"
        all_roles_text = ", ".join(all_roles) if all_roles else "Keine Rollen vorhanden"

        embed = discord.Embed(
            title="Rollenübersicht",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Deine Rollen",
            value=user_roles_text,
            inline=False
        )

        embed.add_field(
            name="Alle Server-Rollen",
            value=all_roles_text,
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Roles(bot))