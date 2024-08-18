import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta
import re
import json
import os

class Shield(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MESSAGE_LIMIT = 5
        self.JOIN_LIMIT = 10
        self.TIME_WINDOW = timedelta(seconds=10)
        self.MUTE_DURATION = timedelta(minutes=30)
        self.LOG_CHANNEL_ID = 1263145025546616995  # Replace with your log channel ID
        self.ADMIN_ROLE_ID = 1260575287960408116  # Replace with your admin role ID
        self.WHITELIST_FILE = "whitelist.json"
        self.SPAM_PATTERNS = [
            r'(.)\1{4,}',  # Repeated characters
            r'\b(?:https?|ftp):\/\/(?:www\.)?[^\s/$.?#].[^\s]*\b',  # Links
            r'\b(?:https?:\/\/)?(?:bit\.ly|goo\.gl|tinyurl\.com|t\.co|short\.ly|ow\.ly|rebrand\.ly|clkim\.com|cutt\.ly|shrt\.co|smi\.ly|is\.gd|buff\.ly|prnt\.sc|adf\.ly|linktr\.ee|l\.ink|bity\.com|bmc\.li|g\.co|shorte\.st|c\.ly|l\.ink|snip\.ly|dld\.ee|pnt\.ly)\b[^\s]*\b',  # Shortened URLs
            r'\b(?:free|win|winner|prize|cash|gift|claim|click|buy|cheap|limited\s+time|urgent|act\s+now|exclusive|offer|sale|deal|promotion|discount)\b',  # Spammy keywords
            r'\b(?:[\w\s]{5,}\s*){3,}\b',  # Repetitive patterns
            r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/~`\\|]{3,}',  # Excessive punctuation
            r'\b(?:%[0-9A-Fa-f]{2}){2,}'  # URL-encoded links
        ]

        self.message_counts = defaultdict(lambda: deque(maxlen=self.MESSAGE_LIMIT))
        self.join_times = deque(maxlen=self.JOIN_LIMIT)
        self.mute_queue = deque()
        self.spam_messages = defaultdict(list)

        if os.path.exists(self.WHITELIST_FILE):
            with open(self.WHITELIST_FILE, 'r') as f:
                self.whitelist = json.load(f)
        else:
            self.whitelist = {"users": [], "links": []}

        self.check_mute_queue.start()

    def save_whitelist(self):
        with open(self.WHITELIST_FILE, 'w') as f:
            json.dump(self.whitelist, f, indent=4)

    @tasks.loop(seconds=10)
    async def check_mute_queue(self):
        now = datetime.utcnow()
        while self.mute_queue and self.mute_queue[0][1] < now:
            user_id = self.mute_queue.popleft()[0]
            guild = self.bot.get_guild(self.bot.guilds[0].id)
            member = guild.get_member(user_id)
            if member:
                try:
                    await member.timeout(None, reason="Temporary mute expired")
                    await self.delete_spam_messages(user_id)
                    await self.log_action(f'Unmuted user {member.mention} after temporary mute.', danger=False)
                except discord.Forbidden:
                    await self.log_action(f'Failed to unmute user {member.mention}. Missing permissions.', danger=True)
                except discord.HTTPException as e:
                    await self.log_action(f'Failed to unmute user {member.mention}. HTTP Exception: {e}', danger=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author.id in self.whitelist["users"]:
            return

        user_id = message.author.id
        now = datetime.utcnow()
        self.message_counts[user_id].append(now)

        if self.is_spam(message.content):
            self.spam_messages[user_id].append(message.id)
            await self.timeout_member(message.author, "Spamming messages")
            return

        if len(self.message_counts[user_id]) >= self.MESSAGE_LIMIT and (now - self.message_counts[user_id][0]) < self.TIME_WINDOW:
            self.spam_messages[user_id].append(message.id)
            await self.timeout_member(message.author, "Spamming messages")
            return

        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id in self.whitelist["users"]:
            return

        now = datetime.utcnow()
        self.join_times.append(now)

        if len(self.join_times) >= self.JOIN_LIMIT and (now - self.join_times[0]) < self.TIME_WINDOW:
            await self.timeout_member(member, "Joining too quickly (potential raid)")

    async def timeout_member(self, member, reason):
        guild = member.guild
        try:
            await member.timeout(self.MUTE_DURATION, reason=reason)
            await self.log_action(f'Timed out user {member.mention} for {reason}', danger=True)
            self.mute_queue.append((member.id, datetime.utcnow() + self.MUTE_DURATION))
        except discord.Forbidden:
            await self.log_action(f'Failed to timeout user {member.mention}. Missing permissions.', danger=True)
        except discord.HTTPException as e:
            await self.log_action(f'Failed to timeout user {member.mention}. HTTP Exception: {e}', danger=True)

    async def delete_spam_messages(self, user_id):
        channel = self.bot.get_channel(self.LOG_CHANNEL_ID)  # Replace with the channel where messages were sent
        for message_id in self.spam_messages.get(user_id, []):
            try:
                msg = await channel.fetch_message(message_id)
                await msg.delete()
                await self.log_action(f'Deleted spam message by user {user_id}', danger=False)
            except discord.Forbidden:
                await self.log_action(f'Failed to delete spam message by user {user_id}. Missing permissions.', danger=True)
            except discord.HTTPException as e:
                await self.log_action(f'Failed to delete spam message by user {user_id}. HTTP Exception: {e}', danger=True)
        self.spam_messages[user_id] = []

    def is_spam(self, content):
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in self.SPAM_PATTERNS)

    async def log_action(self, message, danger=False):
        log_channel = self.bot.get_channel(self.LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🚨 Danger Alert" if danger else "Log",
                description=message,
                color=discord.Color.red() if danger else discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Moderator", value=self.MODERATOR_EMOJI, inline=False)
            embed.add_field(name="User", value=self.USER_EMOJI, inline=False)
            embed.add_field(name="Reason", value=self.REASON_EMOJI, inline=False)
            admin_role = log_channel.guild.get_role(self.ADMIN_ROLE_ID)
            if admin_role:
                await log_channel.send(f'{admin_role.mention}', embed=embed)
            else:
                await log_channel.send(embed=embed)

    MODERATOR_EMOJI = '<:moderators:1263881050116067379>'
    USER_EMOJI = '<:user:1263881179736834101>'
    REASON_EMOJI = '<:reason:1263881245704847476>'

    @app_commands.command(name="whitelist_show", description="Show the whitelist")
    async def whitelist_show(self, interaction: discord.Interaction):
        users = [f"<@{user_id}>" for user_id in self.whitelist["users"]]
        links = self.whitelist["links"]
        await interaction.response.send_message(f"**Whitelisted Users:**\n{', '.join(users)}\n\n**Whitelisted Links:**\n{', '.join(links)}")

    @app_commands.command(name="whitelist_add_user", description="Add a user to the whitelist")
    async def whitelist_add_user(self, interaction: discord.Interaction, user: discord.User):
        if user.id not in self.whitelist["users"]:
            self.whitelist["users"].append(user.id)
            self.save_whitelist()
            await interaction.response.send_message(f"User {user.mention} added to the whitelist.")
        else:
            await interaction.response.send_message(f"User {user.mention} is already in the whitelist.")

    @app_commands.command(name="whitelist_remove_user", description="Remove a user from the whitelist")
    async def whitelist_remove_user(self, interaction: discord.Interaction, user: discord.User):
        if user.id in self.whitelist["users"]:
            self.whitelist["users"].remove(user.id)
            self.save_whitelist()
            await interaction.response.send_message(f"User {user.mention} removed from the whitelist.")
        else:
            await interaction.response.send_message(f"User {user.mention} is not in the whitelist.")

    @app_commands.command(name="whitelist_add_link", description="Add a link to the whitelist")
    async def whitelist_add_link(self, interaction: discord.Interaction, link: str):
        if link not in self.whitelist["links"]:
            self.whitelist["links"].append(link)
            self.save_whitelist()
            await interaction.response.send_message(f"Link {link} added to the whitelist.")
        else:
            await interaction.response.send_message(f"Link {link} is already in the whitelist.")

    @app_commands.command(name="whitelist_remove_link", description="Remove a link from the whitelist")
    async def whitelist_remove_link(self, interaction: discord.Interaction, link: str):
        if link in self.whitelist["links"]:
            self.whitelist["links"].remove(link)
            self.save_whitelist()
            await interaction.response.send_message(f"Link {link} removed from the whitelist.")
        else:
            await interaction.response.send_message(f"Link {link} is not in the whitelist.")

