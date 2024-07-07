import discord
from discord.ext import commands
from datetime import timedelta
import config

EMBEDCOLOR = config.COLOR

class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        try:
            until = timedelta(minutes=duration)
            await member.timeout(until, reason=reason)
            embed = discord.Embed(
        title="",
        description=f"{member} has been muted for {duration} minute(s).",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
            await self.log_action(ctx.guild, "Mute", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send("I do not have permission to mute members.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to mute {member}: {e}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        try:
            await member.timeout(None)
            embed = discord.Embed(
        title="",
        description=f"{member} has been unmuted.",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
            
            await self.log_action(ctx.guild, "Unmute", member, ctx.author)
        except discord.Forbidden:
            await ctx.send("I do not have permission to unmute members.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to unmute {member}: {e}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
        title="",
        description=f"{member} has been kicked.",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
            
            await self.log_action(ctx.guild, "Kick", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send("I do not have permission to kick members.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to kick {member}: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
        title="",
        description=f"{member} has been banned.",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
            await self.log_action(ctx.guild, "Ban", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send("I do not have permission to ban members.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to ban {member}: {e}")



    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(
        title="",
        description=f"{channel.mention} has been locked.",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)
        
        await self.log_action(ctx.guild, "Lock", channel, ctx.author)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(
        title="",
        description=f"{channel.mention} has been unlocked.",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, "Unlock", channel, ctx.author)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"Purged {limit} messages.", delete_after=2)
        await self.log_action(ctx.guild, "Purge", ctx.channel, ctx.author, reason=f"Purged {limit} messages")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(
        title="",
        description=f"Slowmode has been set to {seconds} seconds.",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)
       
        await self.log_action(ctx.guild, "Slowmode", channel, ctx.author, reason=f"Set to {seconds} seconds")

    async def log_action(self, guild, action, target, author, reason=None):
        log_channel_id = config.LOG_CHANNEL_ID
        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(title="Moderation Log", color=discord.Color.blue(), timestamp=discord.utils.utcnow())
            embed.add_field(name="Action", value=action)
            embed.add_field(name="Target", value=target.mention)
            embed.add_field(name="Author", value=author.mention)
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))