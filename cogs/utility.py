import discord
from discord.ext import commands
import config

EMBEDCOLOR = config.COLOR

class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user: discord.User = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"{user}'s Avatar", color=EMBEDCOLOR)
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(description='Show user\'s banner')
    async def banner(self, ctx, user: discord.User = None):
        user = user or ctx.author
        try:
            # Fetch the user within the guild to get the banner
            guild_user = await ctx.guild.fetch_member(user.id)
            if guild_user:
                if guild_user.banner:
                    embed = discord.Embed(title=f"{user}'s Banner", color=EMBEDCOLOR)
                    embed.set_image(url=guild_user.banner.url)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"{user} does not have a banner set.")
            else:
                await ctx.send(f"{user} was not found in this server.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while fetching the banner: {e}")
        except discord.NotFound:
            await ctx.send(f"{user} was not found in this server.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @banner.error
    async def banner_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("User not found or invalid user provided.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("I don't have permission to view the user's banner.")
        elif isinstance(error, commands.CommandInvokeError):
            original_error = error.original
            if isinstance(original_error, discord.Forbidden):
                await ctx.send("I don't have permission to fetch that user's banner.")
            elif isinstance(original_error, discord.HTTPException):
                await ctx.send(f"An HTTP error occurred: {original_error}")
            else:
                await ctx.send(f"An error occurred: {original_error}")
        else:
            await ctx.send(f"An error occurred: {error}")

    @commands.command()
    async def servericon(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}'s Icon", color=EMBEDCOLOR)
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverbanner(self, ctx):
        try:
            banner_url = await ctx.guild.banner_url_as(format="png")
            embed = discord.Embed(title=f"{ctx.guild.name}'s Banner", color=EMBEDCOLOR)
            embed.set_image(url=banner_url)
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(f"{ctx.guild.name} does not have a banner.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
        title="",
        description=f'Pong! Latency: {latency}ms',
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)


    @commands.command(aliases=['mc'])
    async def membercount(self, ctx):
        total_members = ctx.guild.member_count
        total_bots = sum(member.bot for member in ctx.guild.members)
        total_humans = total_members - total_bots
        embed = discord.Embed(title="Member Count", color=EMBEDCOLOR)
        embed.add_field(name="Total Members", value=total_members)
        embed.add_field(name="Total Humans", value=total_humans)
        embed.add_field(name="Total Bots", value=total_bots)
        await ctx.send(embed=embed)

    @commands.command()
    async def inrole(self, ctx, *, role: discord.Role):
        members_with_role = [member for member in ctx.guild.members if role in member.roles]
        embed = discord.Embed(
        title="",
        description=f"Total members with {role.name} : {len(members_with_role)}",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Utility(bot))

