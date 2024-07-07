import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import config

# Constants
EMBEDCOLOR = config.COLOR
PRIVATE_CHANNEL_ID = 1234611667523076176
COUNT_FILE = 'gossip_count.json'

# Helper functions
def get_count():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            data = json.load(f)
            return data.get('count', 0)
    return 0

def increment_count():
    count = get_count() + 1
    with open(COUNT_FILE, 'w') as f:
        json.dump({'count': count}, f)
    return count

class Miscellaneous(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages = {}  # Store deleted messages by channel ID

    @app_commands.command(name='timediff', description='Checks the time difference between the given message IDs.')
    async def timediff(self, interaction: discord.Interaction, message_id1: int, message_id2: int):
        try:
            message1 = await interaction.channel.fetch_message(message_id1)
            message2 = await interaction.channel.fetch_message(message_id2)
            time_diff = abs((message1.created_at - message2.created_at).total_seconds())
            embed = discord.Embed(
                title="Time Difference",
                description=f"The time difference is {time_diff:.2f} seconds.",
                color=EMBEDCOLOR
            )
            await interaction.response.send_message(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(
                title="Error",
                description="One or both of the message IDs provided are not found.",
                color=EMBEDCOLOR
            )
            await interaction.response.send_message(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"An HTTP error occurred: {e}",
                color=EMBEDCOLOR
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An unexpected error occurred: {e}",
                color=EMBEDCOLOR
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name='dm', description='Sends a direct message to the mentioned user with the specified message.')
    async def dm(self, interaction: discord.Interaction, user: discord.User, *, message: str):
        try:
            embed = discord.Embed(
                description=message,
                color=0xcdb5ff  # Corrected color assignment
            )
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await user.send(embed=embed)
            await interaction.response.send_message(f"Message sent to {user.name}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Failed to send message. The user may have DMs disabled or blocked.", ephemeral=True)

    @app_commands.command(name='say', description='Makes the bot say the specified message.')
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("MESSAGE SENT", ephemeral=True)
        await interaction.channel.send(message)

    @app_commands.command(name='embed', description='Makes the bot embed the specified message.')
    @commands.has_permissions(manage_messages=True)
    async def embed(self, interaction: discord.Interaction, *, message: str):
        embed = discord.Embed(
            title="",
            description=message,
            color=EMBEDCOLOR
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild:  # Check if message is in a guild
            channel_id = message.channel.id
            if channel_id not in self.deleted_messages:
                self.deleted_messages[channel_id] = []
            self.deleted_messages[channel_id].append(message)

    @app_commands.command(name='connect', description='Connects to the specified voice channel.')
    async def connect(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        embed = discord.Embed(
            title="",
            description=f"Connected to {channel.name}.",
            color=EMBEDCOLOR
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gossip", description="Send a secret gossip to a private channel.")
    async def gossip(self, interaction: discord.Interaction, message: str):
        private_channel = self.bot.get_channel(PRIVATE_CHANNEL_ID)
        if private_channel is None:
            await interaction.response.send_message("Private channel not found.", ephemeral=True)
            return

        count = increment_count()
        embed = discord.Embed(
            title=f"Gossip #{count}",
            description=message,
            color=EMBEDCOLOR
        )
        guild = interaction.guild
        if guild and guild.icon:
            embed.set_footer(text=".gg/bitvches | Use /gossip to send your gossips anonymously", icon_url=guild.icon.url)
        else:
            embed.set_footer(text=".gg/bitvches | Use /gossip to send your gossips anonymously")

        await private_channel.send(embed=embed)
        await interaction.response.send_message("Your gossip has been sent!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
