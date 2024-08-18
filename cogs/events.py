import discord
from discord.ext import commands
from datetime import datetime
import config

# Configuration
MESSAGE_LOG_CHANNEL_ID = 1267718912259264625  # Replace with your message log channel ID
SERVER_LOG_CHANNEL_ID = 1259466841059889154   # Replace with your server log channel ID
JOINLEAVE = 1259466840254582887               # Replace with your join/leave log channel ID
EMBEDCOLOR = config.EMBED_COLOR

class MessageLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def create_embed(self, title, description=None):
        embed = discord.Embed(
            title=title,
            color=EMBEDCOLOR,
            description=description,
            timestamp=datetime.utcnow()
        )
        return embed

    # Message Events
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Message Edited")
        embed.set_author(name=before.author.display_name, icon_url=before.author.avatar.url)
        embed.add_field(name="User", value=before.author.mention, inline=True)
        embed.add_field(name="User ID", value=before.author.id, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Channel ID", value=before.channel.id, inline=True)
        embed.add_field(name="Before", value=before.content if before.content else "[Embed/Attachment]", inline=False)
        embed.add_field(name="After", value=after.content if after.content else "[Embed/Attachment]", inline=False)
        embed.add_field(name="Edited at", value=f"<t:{timestamp}>", inline=False)
        
        if before.attachments:
            embed.add_field(name="Before Attachment", value=before.attachments[0].url, inline=False)
        if after.attachments:
            embed.add_field(name="After Attachment", value=after.attachments[0].url, inline=False)
        
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send edit log: {e}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Message Deleted")
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.add_field(name="User", value=message.author.mention, inline=True)
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Channel ID", value=message.channel.id, inline=True)
        embed.add_field(name="Content", value=message.content if message.content else "[Embed/Attachment]", inline=False)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        if message.attachments:
            embed.add_field(name="Attachment", value=message.attachments[0].url, inline=False)
        
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send delete log: {e}")

    # Member Events
    @commands.Cog.listener()
    async def on_member_join(self, member):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Member Joined")
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(JOINLEAVE)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send member join log: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Member Left")
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Left at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(JOINLEAVE)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send member leave log: {e}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Member Banned")
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Banned at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send ban log: {e}")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Member Unbanned")
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Unbanned at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send member unban log: {e}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Member Updated")
        embed.set_author(name=after.display_name, icon_url=after.avatar.url)
        embed.add_field(name="User", value=after.mention, inline=True)
        embed.add_field(name="User ID", value=after.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.nick != after.nick:
            embed.add_field(name="Nickname Before", value=before.nick if before.nick else "None", inline=True)
            embed.add_field(name="Nickname After", value=after.nick if after.nick else "None", inline=True)
        
        if before.roles != after.roles:
            before_roles = ", ".join([role.name for role in before.roles])
            after_roles = ", ".join([role.name for role in after.roles])
            embed.add_field(name="Roles Before", value=before_roles, inline=False)
            embed.add_field(name="Roles After", value=after_roles, inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send member update log: {e}")

    # Channel Events
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Channel Created")
        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon.url)
        embed.add_field(name="Channel", value=channel.mention, inline=True)
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        embed.add_field(name="Created at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send channel creation log: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Channel Deleted")
        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon.url)
        embed.add_field(name="Channel", value=channel.name, inline=True)
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send channel deletion log: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Channel Updated")
        embed.set_author(name=before.guild.name, icon_url=before.guild.icon.url)
        embed.add_field(name="Channel", value=before.mention, inline=True)
        embed.add_field(name="Channel ID", value=before.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.name != after.name:
            embed.add_field(name="Name Before", value=before.name, inline=True)
            embed.add_field(name="Name After", value=after.name, inline=True)
        
        if before.topic != after.topic:
            embed.add_field(name="Topic Before", value=before.topic if before.topic else "None", inline=True)
            embed.add_field(name="Topic After", value=after.topic if after.topic else "None", inline=True)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send channel update log: {e}")

    # Role Events
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Role Created")
        embed.set_author(name=role.guild.name, icon_url=role.guild.icon.url)
        embed.add_field(name="Role", value=role.mention, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Created at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send role creation log: {e}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Role Deleted")
        embed.set_author(name=role.guild.name, icon_url=role.guild.icon.url)
        embed.add_field(name="Role", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send role deletion log: {e}")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Role Updated")
        embed.set_author(name=before.guild.name, icon_url=before.guild.icon.url)
        embed.add_field(name="Role", value=before.mention, inline=True)
        embed.add_field(name="Role ID", value=before.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.name != after.name:
            embed.add_field(name="Name Before", value=before.name, inline=True)
            embed.add_field(name="Name After", value=after.name, inline=True)
        
        if before.permissions != after.permissions:
            embed.add_field(name="Permissions Before", value=str(before.permissions), inline=False)
            embed.add_field(name="Permissions After", value=str(after.permissions), inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send role update log: {e}")

    # Voice State Events
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Voice State Updated")
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.channel != after.channel:
            embed.add_field(name="Channel Before", value=before.channel.mention if before.channel else "None", inline=True)
            embed.add_field(name="Channel After", value=after.channel.mention if after.channel else "None", inline=True)
        
        if before.self_mute != after.self_mute:
            embed.add_field(name="Self Mute Before", value=str(before.self_mute), inline=True)
            embed.add_field(name="Self Mute After", value=str(after.self_mute), inline=True)
        
        if before.self_deaf != after.self_deaf:
            embed.add_field(name="Self Deaf Before", value=str(before.self_deaf), inline=True)
            embed.add_field(name="Self Deaf After", value=str(after.self_deaf), inline=True)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send voice state update log: {e}")

    # Server Events
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Guild Updated")
        embed.set_author(name=before.name, icon_url=before.icon.url)
        embed.add_field(name="Guild ID", value=before.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.name != after.name:
            embed.add_field(name="Name Before", value=before.name, inline=True)
            embed.add_field(name="Name After", value=after.name, inline=True)
        
        if before.region != after.region:
            embed.add_field(name="Region Before", value=str(before.region), inline=True)
            embed.add_field(name="Region After", value=str(after.region), inline=True)
        
        if before.owner != after.owner:
            embed.add_field(name="Owner Before", value=before.owner.mention, inline=True)
            embed.add_field(name="Owner After", value=after.owner.mention, inline=True)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send guild update log: {e}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Guild Joined")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send guild join log: {e}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Guild Removed")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Removed at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send guild remove log: {e}")

    # Reaction Events
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Reaction Added")
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Channel", value=reaction.message.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=reaction.message.id, inline=True)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=True)
        embed.add_field(name="Added at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send reaction add log: {e}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Reaction Removed")
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Channel", value=reaction.message.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=reaction.message.id, inline=True)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=True)
        embed.add_field(name="Removed at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send reaction remove log: {e}")

    # Emoji Events
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Emojis Updated")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        before_emojis = ", ".join([emoji.name for emoji in before])
        after_emojis = ", ".join([emoji.name for emoji in after])
        embed.add_field(name="Emojis Before", value=before_emojis, inline=False)
        embed.add_field(name="Emojis After", value=after_emojis, inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send emojis update log: {e}")

    @commands.Cog.listener()
    async def on_guild_emoji_create(self, emoji):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Emoji Created")
        embed.set_author(name=emoji.guild.name, icon_url=emoji.guild.icon.url)
        embed.add_field(name="Emoji", value=emoji.name, inline=True)
        embed.add_field(name="Emoji ID", value=emoji.id, inline=True)
        embed.add_field(name="Created at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send emoji create log: {e}")

    @commands.Cog.listener()
    async def on_guild_emoji_delete(self, emoji):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Emoji Deleted")
        embed.set_author(name=emoji.guild.name, icon_url=emoji.guild.icon.url)
        embed.add_field(name="Emoji", value=emoji.name, inline=True)
        embed.add_field(name="Emoji ID", value=emoji.id, inline=True)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send emoji delete log: {e}")

    # Invite Events
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Invite Created")
        embed.set_author(name=invite.guild.name, icon_url=invite.guild.icon.url)
        embed.add_field(name="Invite Code", value=invite.code, inline=True)
        embed.add_field(name="Channel", value=invite.channel.mention, inline=True)
        embed.add_field(name="Created at", value=f"<t:{timestamp}>", inline=False)
        
        if invite.inviter:
            embed.add_field(name="Inviter", value=invite.inviter.mention, inline=True)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send invite create log: {e}")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Invite Deleted")
        embed.set_author(name=invite.guild.name, icon_url=invite.guild.icon.url)
        embed.add_field(name="Invite Code", value=invite.code, inline=True)
        embed.add_field(name="Channel", value=invite.channel.mention, inline=True)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send invite delete log: {e}")

    # Integration Events
    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Integrations Updated")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send integrations update log: {e}")

    # Thread Events
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Thread Created")
        embed.set_author(name=thread.guild.name, icon_url=thread.guild.icon.url)
        embed.add_field(name="Thread", value=thread.name, inline=True)
        embed.add_field(name="Thread ID", value=thread.id, inline=True)
        embed.add_field(name="Created at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send thread create log: {e}")

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Thread Updated")
        embed.set_author(name=before.guild.name, icon_url=before.guild.icon.url)
        embed.add_field(name="Thread", value=before.name, inline=True)
        embed.add_field(name="Thread ID", value=before.id, inline=True)
        embed.add_field(name="Updated at", value=f"<t:{timestamp}>", inline=False)
        
        if before.name != after.name:
            embed.add_field(name="Name Before", value=before.name, inline=True)
            embed.add_field(name="Name After", value=after.name, inline=True)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send thread update log: {e}")

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Thread Deleted")
        embed.set_author(name=thread.guild.name, icon_url=thread.guild.icon.url)
        embed.add_field(name="Thread", value=thread.name, inline=True)
        embed.add_field(name="Thread ID", value=thread.id, inline=True)
        embed.add_field(name="Deleted at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send thread delete log: {e}")

    @commands.Cog.listener()
    async def on_thread_member_join(self, thread, member):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Thread Member Joined")
        embed.set_author(name=thread.guild.name, icon_url=thread.guild.icon.url)
        embed.add_field(name="Thread", value=thread.name, inline=True)
        embed.add_field(name="Thread ID", value=thread.id, inline=True)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send thread member join log: {e}")

    @commands.Cog.listener()
    async def on_thread_member_remove(self, thread, member):
        timestamp = int(datetime.utcnow().timestamp())

        embed = self.create_embed("Thread Member Removed")
        embed.set_author(name=thread.guild.name, icon_url=thread.guild.icon.url)
        embed.add_field(name="Thread", value=thread.name, inline=True)
        embed.add_field(name="Thread ID", value=thread.id, inline=True)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Removed at", value=f"<t:{timestamp}>", inline=False)
        
        log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to send thread member remove log: {e}")
            
async def setup(bot):
    await bot.add_cog(MessageLogging(bot))
