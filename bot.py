import discord
from discord.ext import commands

import config  # Import your configuration module
import logging
import json
import time
from discord.ui import View, Select

# Set up logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
intents.members = True

BOT_TOKEN = config.BOT_TOKEN
WELCOME_CHANNEL_ID = config.WELCOME_CHANNEL_ID
LEAVE_CHANNEL_ID = config.LEAVE_CHANNEL_ID
LOG_CHANNEL_ID = config.LOG_CHANNEL_ID
EMBED_COLOR = config.EMBED_COLOR
OWNER_ID = config.OWNER_ID

class HelpDropdown(Select):
    def __init__(self, help_command, cogs):
        self.help_command = help_command
        options = [
            discord.SelectOption(label=cog.qualified_name, description=cog.description or "No description")
            for cog in cogs if cog
        ]
        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cog_name = self.values[0]
        cog = self.help_command.context.bot.get_cog(cog_name)
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            description=cog.description or "No description available.",
            color=EMBED_COLOR
        )
        for command in cog.get_commands():
            if not command.hidden:
                embed.add_field(name=command.name, value=command.help or "No description available.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(View):
    def __init__(self, help_command, cogs):
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(help_command, cogs))

class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        cogs = [cog for cog in mapping.keys() if cog]
        view = HelpView(self, cogs)
        guild = self.context.guild
        embed = discord.Embed(
            title="Bot Commands",
            description="Select a category from the dropdown to view commands.",
            color=EMBED_COLOR,
            timestamp=discord.utils.utcnow()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Total Members", value=guild.member_count, inline=True)
        embed.add_field(name="Server Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Server Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="FOUNDER", value=f"<@{OWNER_ID}>", inline=True)  # Use OWNER_ID from config
        embed.set_footer(text="Use the dropdown menu to navigate through the commands.")
        await self.get_destination().send(embed=embed, view=view)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help with `{command.name}`", description=command.help or "No description available.", color=EMBED_COLOR)
        embed.add_field(name="Usage", value=self.get_command_signature(command))
        await self.get_destination().send(embed=embed)

bot = commands.Bot(command_prefix='?', intents=intents, help_command=CustomHelpCommand())

async def load_extensions():
    initial_extensions = [
        'cogs.moderation', 
        'cogs.utility',
        'cogs.role',
        'cogs.Miscellaneous'
    ]
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"\033[92mLoaded extension:\033[0m \033[94m{extension}\033[0m")
        except Exception as e:
            print(f"\033[91mFailed to load extension {extension}: {e}\033[0m")

afk_data = {}

async def load_db():
    global afk_data
    try:
        with open('db.json', 'r') as f:
            afk_data = json.load(f)
    except FileNotFoundError:
        afk_data = {}

async def save_db():
    global afk_data
    with open('db.json', 'w') as f:
        json.dump(afk_data, f, indent=4)

def create_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

def send_normal_message(channel, message):
    return channel.send(message)

def send_embed_message(channel, title, description, color):
    embed = create_embed(title, description, color)
    return channel.send(embed=embed)

@bot.before_invoke
async def before_any_command(ctx):
    await load_db()

@bot.command(name='afk', description='Set your AFK status with a reason.')
async def afk(interaction: discord.Interaction, reason: str = "None"):
    user = interaction.user
    user_id = str(user.id)
    afk_data[user_id] = {
        'reason': reason,
        'status': 1,
        'timestamp': int(time.time()),
        'mentions': []
    }
    with open('db.json', 'w') as f:
        json.dump(afk_data, f, indent=4)
    message = f"{user.mention} is now AFK: {reason}"

    embed = create_embed("AFK", message, EMBED_COLOR)
    embed.set_author(name=user.display_name, icon_url=user.avatar.url or discord.Embed.Empty)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if user_id in afk_data:
        if afk_data[user_id]['status'] == 1:
            afk_data[user_id]['status'] = 0
            afk_start = afk_data[user_id]['timestamp']
            afk_end = int(time.time())
            afk_duration = afk_end - afk_start
            mentions_info = afk_data[user_id].get('mentions', [])
            afk_data[user_id]['mentions'] = []
            await save_db()

            back_message = f"Welcome back {message.author.mention}. You were AFK for {int(afk_duration // 60)} minutes and {int(afk_duration % 60)} seconds."
            
            if mentions_info:
                mentions_embed = discord.Embed(
                    title=f"You have {len(mentions_info)} mention(s)",
                    color=EMBED_COLOR
                )
                for mention in mentions_info:
                    mention_field_name = f"By {mention['author']}, <t:{mention['timestamp']}:R>"
                    mention_field_value = f"[Click to View Message]({mention['url']})"
                    mentions_embed.add_field(name=mention_field_name, value=mention_field_value, inline=False)
                
                await message.channel.send(back_message, embed=mentions_embed)
            else:
                await message.channel.send(back_message)

    mentions = message.mentions
    for mention in mentions:
        mention_id = str(mention.id)
        if mention_id in afk_data and afk_data[mention_id]['status'] == 1:
            afk_message = f"{mention.name} is currently AFK: {afk_data[mention_id]['reason']} - <t:{afk_data[mention_id]['timestamp']}:R>"
            await message.channel.send(afk_message)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = member.guild.get_role(config.ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f'Assigned role with ID {config.ROLE_ID} to {member.name}')
    else:
        print(f'Role with ID {config.ROLE_ID} not found')

    channel = bot.get_channel(config.WELCOME_CHANNEL_ID)
    if channel is not None:
        embed = discord.Embed(
            title="Welcome!",
            description=f"Hello {member.mention} ({member.name}), welcome to {guild.name}! We're glad to have you here.",
            color=EMBED_COLOR,
            timestamp=discord.utils.utcnow()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Enjoy your stay!")
        await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.premium_since is None and after.premium_since is not None:
        channel = bot.get_channel(config.LOG_CHANNEL_ID)
        
        if channel:
            embed = discord.Embed(
                title="Server Boosted!",
                description=f"{after.mention} has boosted the server!",
                color=EMBED_COLOR
            )
            embed.set_author(name=after.name, icon_url=after.avatar.url)
            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = bot.get_channel(config.LEAVE_CHANNEL_ID)
    if channel is not None:
        embed = discord.Embed(
            title="Goodbye!",
            description=f"{member.mention} ({member.name}) has left {guild.name}. We'll miss you!",
            color=EMBED_COLOR,
            timestamp=discord.utils.utcnow()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Hope to see you again!")
        await channel.send(embed=embed)

@bot.event
async def on_ready():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\033[92mLogged in as {bot.user}\033[0m')
    print(f'\033[92mBot is connected to the following guilds:\033[0m')
    for guild in bot.guilds:
        print(f'\033[94m - {guild.name}\033[0m (\033[94mID: {guild.id}\033[0m)')
    await bot.tree.sync()
    num_commands = len(bot.commands)
    print(f'\033[92mSynced {num_commands} commands.\033[0m')
    print('\033[95mDeveloped by \033[0m\033s Numan.\033[0m \033[95m(1240349397053603870)\033[0m')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.BOT_TOKEN)

import asyncio
asyncio.run(main())
