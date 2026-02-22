import discord
from discord import app_commands
from discord.ext import commands


class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="createchannel",
        description="Erstellt einen privaten Channel in einer bestehenden Kategorie"
    )
    @app_commands.describe(
        channel_name="Name des neuen Channels",
        category_name="Name der existierenden Kategorie",
        channel_type="Art des Channels (text oder voice)"
    )
    @app_commands.choices(
        channel_type=[
            app_commands.Choice(name="Text", value="text"),
            app_commands.Choice(name="Voice", value="voice")
        ]
    )
    async def create_channel(
        self,
        interaction: discord.Interaction,
        channel_name: str,
        category_name: str,
        channel_type: app_commands.Choice[str]
    ):
        guild = interaction.guild

        if guild is None:
            category = await guild.create_category(
                name=category_name, 
                reason="Automatisch erstellt durch /createchannel"
            )
            

        category = discord.utils.get(guild.categories, name=category_name)

        if category is None:
            category = await guild.create_category(
                name=category_name,
                reason="Automatisch erstellt durch /createchannel"
            )
        
        channel_name = channel_name.lower().replace(" ", "-")   

        role = await guild.create_role(
            name=f"{channel_name}_role",
            reason="Private Channel Role"
        )

        await interaction.user.add_roles(role)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                connect=True,
                speak=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True
            )
        }

        if channel_type.value == "text":
            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )
        else:
            channel = await guild.create_voice_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )

        await interaction.response.send_message(
            f"Privater Channel {channel.mention} wurde erstellt.\n"
            f"Rolle {role.name} wurde dir zugewiesen.",
            ephemeral=True
        )

async def setup(bot):
    cog = ChannelManager(bot)
    await bot.add_cog(cog)
    try:
        bot.tree.add_command(cog.create_channel)
    except app_commands.CommandAlreadyRegistered:
        pass