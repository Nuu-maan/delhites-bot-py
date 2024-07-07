import discord
from discord.ext import commands
import config

EMBEDCOLOR = config.COLOR
x = 1

class Role(commands.Cog, name="Role"):
    def __init__(self, bot):
        self.bot = bot

    async def can_manage_roles(self, ctx):
        """Checks if the user has the 'manage roles' permission."""
        author = ctx.author
        if isinstance(ctx.channel, discord.DMChannel) or not isinstance(ctx.author, discord.Member):
            return False
        return ctx.channel.permissions_for(author).manage_roles

    @commands.command(name='createrole')
    async def create_role(self, ctx, *, role_name):
        """Creates a new role with the specified name."""
        if await self.can_manage_roles(ctx):
            try:
                await ctx.guild.create_role(name=role_name)
                embed = discord.Embed(
        title="",
        description=f"Role `{role_name}` created successfully.",
        color=EMBEDCOLOR
    )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have permission to create roles.")
        else:
            await ctx.send("You don't have permission to manage roles.")

    @commands.command(name='deleterole')
    async def delete_role(self, ctx, *, role: discord.Role):
        """Deletes the specified role."""
        if await self.can_manage_roles(ctx):
            try:
                await role.delete()
                embed = discord.Embed(
        title="",
        description=f"Role `{role.name}` deleted successfully.",
        color=EMBEDCOLOR
    )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have permission to delete roles.")
        else:
            await ctx.send("You don't have permission to manage roles.")

    @commands.command(name='addrole')
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        """Adds a role to the specified user."""
        if await self.can_manage_roles(ctx):
            try:
                await member.add_roles(role)
                embed = discord.Embed(
        title="",
        description=f"Role `{role.name}` added to {member.display_name}.",
        color=EMBEDCOLOR
    )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have permission to add roles.")
        else:
            await ctx.send("You don't have permission to manage roles.")
        


    

async def setup(bot):
    await bot.add_cog(Role(bot))
