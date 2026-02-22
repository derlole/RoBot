import discord
from discord import app_commands
from discord.ext import commands


class ChannelUserManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="adduser",
        description="Fügt einem privaten Channel die Rolle eines Users hinzu"
    )
    @app_commands.describe(
        member="Der User, der Zugriff erhalten soll"
    )
    async def add_user(self, interaction: discord.Interaction, member: discord.Member):
        channel = interaction.channel
        guild = interaction.guild

        if guild is None or not isinstance(channel, discord.abc.GuildChannel):
            await interaction.response.send_message(
                "Dieser Command funktioniert nur in einem Server-Channel.",
                ephemeral=True
            )
            return

        role_name = f"{channel.name}_role"
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None:
            await interaction.response.send_message(
                f"Es gibt keine Rolle für diesen Channel ({role_name}).",
                ephemeral=True
            )
            return

        await member.add_roles(role, reason=f"Zugriff auf privaten Channel {channel.name}")

        await interaction.response.send_message(
            f"{member.mention} wurde Zugriff auf {channel.mention} gegeben.",
            ephemeral=True
        )


async def setup(bot):
    cog = ChannelUserManager(bot)
    await bot.add_cog(cog)
    try:
        bot.tree.add_command(cog.add_user)
    except app_commands.CommandAlreadyRegistered:
        print("add_user Command ist bereits registriert, überspringe Registrierung.")