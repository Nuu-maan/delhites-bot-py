import discord
import random
from discord.ext import commands
import config

EMBEDCOLOR = config.COLOR


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', aliases=['roll'])
    async def roll_dice(self, ctx, num_dice: int = 1, num_sides: int = 6):
        """Rolls a dice with the specified number of sides"""
        if num_dice < 1 or num_sides < 2:
            embed = discord.Embed(
        title="",
        description="Please provide valid parameters.",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
         
            return
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        embed = discord.Embed(
        title="",
        description=f"Rolling {num_dice} dice with {num_sides} sides: {rolls}",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)

    @commands.command(name='coinflip', aliases=['cf'])
    async def coinflip(self, ctx):
        """Flips a coin and returns heads or tails."""
        result = random.choice(['Heads', 'Tails'])
        embed = discord.Embed(
        title="",
        description=f"The coin landed on: {result}",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self, ctx, *choices):
        """Chooses one option from the provided choices."""
        if len(choices) < 2:
            embed = discord.Embed(
        title="",
        description="Please provide at least two choices.",
        color=EMBEDCOLOR
    )
            await ctx.send(embed=embed)
            return
        choice = random.choice(choices)
        embed = discord.Embed(
        title="",
        description=f"My choice is: {choice}",
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)


    @commands.command(name='quote')
    async def quote(self, ctx):
        """Sends a random quote."""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Life is what happens when you're busy making other plans. - John Lennon"
        ]
        quote = random.choice(quotes)
        embed = discord.Embed(
        title="",
        description=quote,
        color=EMBEDCOLOR
    )
        await ctx.send(embed=embed)

    @commands.command(name='rps', aliases=['rock_paper_scissors'])
    async def rps(self, ctx, choice: str):
        """Play rock-paper-scissors against the bot."""
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)
        await ctx.send(embed=discord.Embed(title="", description=f"I choose: {bot_choice}", color=EMBEDCOLOR))

        if choice.lower() == bot_choice:
            await ctx.send(embed=discord.Embed(title="", description="It's a tie!", color=EMBEDCOLOR))

        elif choice.lower() == 'rock' and bot_choice == 'scissors' \
            or choice.lower() == 'paper' and bot_choice == 'rock' \
            or choice.lower() == 'scissors' and bot_choice == 'paper':
            await ctx.send(embed=discord.Embed(title="", description="You win!", color=EMBEDCOLOR))
        else:
            await ctx.send(embed=discord.Embed(title="", description="I win!", color=EMBEDCOLOR))

    @commands.command(name='dice_sum')
    async def dice_sum(self, ctx, num_dice: int = 2, num_sides: int = 6):
        """Rolls multiple dice and returns the sum."""
        if num_dice < 1 or num_sides < 2:
            await ctx.send("Please provide valid parameters.")
            return
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        embed = discord.Embed(
            title="Dice Roll",
            description=f"Rolling {num_dice} dice with {num_sides} sides.",
            color=EMBEDCOLOR
        )
        embed.add_field(name="Total Sum", value=total, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='fact')
    async def fact(self, ctx):
        """Sends a random interesting fact."""
        facts = [
            "A group of flamingos is called a flamboyance.",
            "Honey never spoils.",
            "A day on Venus is longer than a year on Venus.",
            "The shortest war in history lasted only 38 minutes.",
            "Bananas are berries but strawberries aren't.",
            "The unicorn is the national animal of Scotland."
        ]
        fact = random.choice(facts)
        embed = discord.Embed(
            title="Random Fact",
            description=fact,
            color=EMBEDCOLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name='choose_color')
    async def choose_color(self, ctx):
        """Chooses a random color."""
        colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "black", "white"]
        color = random.choice(colors)
        embed = discord.Embed(
            title="Chosen Color",
            description=f"The chosen color is: {color}",
            color=EMBEDCOLOR
        )
        await ctx.send(embed=embed)

    @commands.command(name='roll_fortune')
    async def roll_fortune(self, ctx):
        """Rolls a fortune."""
        fortunes = [
            "A beautiful, smart, and loving person will be coming into your life.",
            "A dubious friend may be an enemy in camouflage.",
            "A faithful friend is a strong defense.",
            "A fresh start will put you on your way.",
            "A friend asks only for your time not your money.",
            "A friend is a present you give yourself.",
            "A gambler not only will lose what he has, but also will lose what he doesn't have.",
            "A golden egg of opportunity falls into your lap this month."
        ]
        fortune = random.choice(fortunes)
        embed = discord.Embed(
            title="Your Fortune",
            description=fortune,
            color=EMBEDCOLOR
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))