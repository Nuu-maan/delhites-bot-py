import discord
from discord.ext import commands, tasks
import os
import asyncio
import json
import time
import config
from discord.ui import Select, View

intents = discord.Intents.all()
intents.members = True
TRIGGERS_DB_PATH = 'triggers.json'
WELCOME_CHANNEL_ID = 1259466794469691435
LEAVE_CHANNEL_ID = 1259466796201672885
OWNER2 = 1183482904270090311
ROLE_ID = 1259466684800958475
TEMP_CHANNEL_ID = 1259466819555823688
EMBEDCOLOR = 0x2B2D31

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)
invites = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.load_extension('cogs.utility')
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.role')
    await bot.load_extension('cogs.Miscellaneous')
    await bot.load_extension('cogs.events')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    # Start status rotation
    status_rotation.start()

# List of statuses to rotate through
statuses = [
    discord.Activity(type=discord.ActivityType.watching, name="discord.gg/delhites"),
    discord.Activity(type=discord.ActivityType.listening, name="Use ?help"),
    discord.Activity(type=discord.ActivityType.watching, name="Watching your gossips.")
]


@tasks.loop(seconds=10)  # Change status every 10 seconds
async def status_rotation():
    for status in statuses:
        await bot.change_presence(activity=status)
        await asyncio.sleep(10)  # Sleep for 10 seconds before changing to the next status





afk_data = {}

async def load_db():
    global afk_data
    try:
        with open('db.json', 'r') as f:
            afk_data = json.load(f)
    except FileNotFoundError:
        afk_data = {}

# Embed mode variable and configuration
embed_mode = 1
embed_config = {
    "color": EMBEDCOLOR,
    "afk_title": "AFK",
    "afk_back_title": "Welcome Back",
    "afk_notice_title": "AFK Notice"
}

# Make save_db asynchronous
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

@bot.tree.command(name='afk', description='Set your AFK status with a reason.')
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
        json.dump(afk_data, f, indent=4)  # Remove await here
    message = f"{user.mention} is now AFK: {reason}"

    if embed_mode == 1:
        embed = create_embed(embed_config["afk_title"], message, embed_config["color"])
        embed.set_author(name=user.display_name, icon_url=user.avatar.url or discord.Embed.Empty)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(message)

# Traditional command version
@bot.command(name='afk', help='Set your AFK status with a reason.')
async def afk_prefix(ctx, *, reason: str = "None"):
    user = ctx.author
    user_id = str(user.id)
    afk_data[user_id] = {
        'reason': reason,
        'status': 1,
        'timestamp': int(time.time()),  # Store timestamp as an integer
        'mentions': []
    }
    with open('db.json', 'w') as f:
        json.dump(afk_data, f, indent=4) # Remove await here
    message = f"{user.mention} is now AFK: {reason}"

    if embed_mode == 1:
        embed = create_embed(embed_config["afk_title"], message, embed_config["color"])
        embed.set_author(name=user.display_name, icon_url=user.avatar.url or discord.Embed.Empty)
        await ctx.send(embed=embed)
    else:
        await ctx.send(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if user_id in afk_data:
        afk_info = afk_data.get(user_id, {})
        if 'status' in afk_info and afk_info['status'] == 1:
            afk_data[user_id]['status'] = 0
            afk_start = afk_info.get('timestamp', int(time.time()))
            afk_end = int(time.time())
            afk_duration = afk_end - afk_start
            mentions_info = afk_info.get('mentions', [])
            afk_info['mentions'] = []
            afk_data[user_id] = afk_info  # Update afk_data with cleared mentions
            await save_db()

            days, remainder = divmod(afk_duration, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            if days > 0:
                duration_message = f"{days} days, {hours} hours and {minutes} minutes"
            elif hours > 0:
                duration_message = f"{hours} hours and {minutes} minutes"
            else:
                duration_message = f"{minutes} minutes and {seconds} seconds"

            back_message = f"Welcome back {message.author.mention}. You were AFK for {duration_message}."

            if mentions_info:
                mentions_embed = discord.Embed(
                    title=f"You have {len(mentions_info)} mention(s)",
                    color=embed_config["color"]
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
        if mention_id in afk_data:
            mention_info = afk_data.get(mention_id, {})
            if 'status' in mention_info and mention_info['status'] == 1:
                afk_message = f"{mention.name} is currently AFK: {mention_info['reason']} - <t:{mention_info['timestamp']}:R>"
                await message.channel.send(afk_message)

                # Store mention details
                mention_info['mentions'].append({
                    'author': str(message.author),
                    'timestamp': int(time.time()),  # Store timestamp as an integer
                    'url': message.jump_url
                })
                afk_data[mention_id] = mention_info
                await save_db()

    await bot.process_commands(message)




@bot.event
async def on_member_join(member):
    guild = member.guild

    # Assign a role to the member
    try:
        role = guild.get_role(ROLE_ID)
        if role:
            await member.add_roles(role)
            print(f'Assigned role with ID {ROLE_ID} to {member.name}')
        else:
            print(f'Role with ID {ROLE_ID} not found')
    except Exception as e:
        print(f"Error assigning role: {e}")

    inviter = None
    try:
        # Fetch the current invites
        new_invites = await guild.invites()
        old_invites = invites[guild.id]

        # Compare invite counts to find the invite used
        for new_invite in new_invites:
            for old_invite in old_invites:
                if new_invite.code == old_invite.code and new_invite.uses > old_invite.uses:
                    inviter = new_invite.inviter
                    break
            if inviter:
                break

        # Update the stored invites with the current invites
        invites[guild.id] = new_invites
    except Exception as e:
        print(f"Error fetching invites: {e}")

    if inviter:
        inviter_text = f"Invited by {inviter.mention}"
    else:
        inviter_text = "Joined using a vanity URL or unknown invite"

    # Send a welcome message
    try:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is not None:
            embed = discord.Embed(
                title="Welcome!",
                description=(
                    f"Hello {member.mention} ({member.name}), welcome to {guild.name}! "
                    f"We're glad to have you here. {inviter_text}."
                ),
                color=0x2B2D31,
                timestamp=discord.utils.utcnow()
            )
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            embed.set_footer(text="Enjoy your stay!")
            await channel.send(embed=embed)
        else:
            print(f"Channel with ID {WELCOME_CHANNEL_ID} not found")
    except Exception as e:
        print(f"Error sending welcome message: {e}")

    # Send a temporary welcome message
    try:
        temp_channel = bot.get_channel(TEMP_CHANNEL_ID)
        if temp_channel is not None:
            temp_message = await temp_channel.send(f"{member.mention} Welcome to {guild.name}")
            await asyncio.sleep(30)  # Wait for 30 seconds
            await temp_message.delete()
        else:
            print(f"Temporary channel with ID {TEMP_CHANNEL_ID} not found")
    except Exception as e:
        print(f"Error sending temporary message: {e}")

@bot.event
async def on_invite_create(invite):
    # Update invites dictionary when a new invite is created
    invites[invite.guild.id] = await invite.guild.invites()

@bot.event
async def on_invite_delete(invite):
    # Update invites dictionary when an invite is deleted
    invites[invite.guild.id] = await invite.guild.invites()




@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if channel is not None:
        embed = discord.Embed(
            title="Goodbye!",
            description=f"{member.mention} ({member.name}) has left {guild.name}. We'll miss you!",
            color=0x2B2D31,
            timestamp=discord.utils.utcnow()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Hope to see you again!")
        await channel.send(embed=embed)





class HelpSelect(Select):
    def __init__(self, bot, options):
        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        selected_cog = self.values[0]
        cog = self.bot.get_cog(selected_cog)
        if cog:
            commands_list = [
                f'`{command.name}` - {command.description or "No description"}'
                for command in cog.walk_app_commands() if command.name != 'help'
            ]
            embed = discord.Embed(title=f'{cog.qualified_name} Commands', description='\n'.join(commands_list))
            await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        options = [
            discord.SelectOption(label=cog.qualified_name, description=cog.description or 'No description')
            for cog in bot.cogs.values() if cog.qualified_name.lower() != 'helpcommand'
        ]

        # Split options into groups of 25
        for i in range(0, len(options), 25):
            self.add_item(HelpSelect(bot, options[i:i + 25]))


@commands.command()
async def help(ctx):
    """Shows help message"""
    view = HelpView(ctx.bot)
    embed = discord.Embed(
        title="Bot Commands",
        description="Select a category from the dropdown to view commands.",
        color=discord.Color.blue(),
        timestamp=ctx.message.created_at
    )
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Total Members", value=ctx.guild.member_count, inline=True)

    # Use a relative timestamp
    created_at_unix = int(ctx.guild.created_at.timestamp())
    embed.add_field(name="Server Created", value=f"<t:{created_at_unix}:D>", inline=True)

    embed.add_field(name="Server Owner", value=ctx.guild.owner.mention, inline=True)
    embed.add_field(name="FOUNDER", value=f"<@{OWNER2}>", inline=True)
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)  # Set server icon if available
    embed.set_footer(text="Use the dropdown menu to navigate through the commands.")


bot.run("")
