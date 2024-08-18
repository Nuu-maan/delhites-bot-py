import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, InputText, Button, View

class ProfileSetupModal(Modal):
    def __init__(self):
        super().__init__(title="Profile Setup")

        self.add_item(InputText(label="Bio", placeholder="Tell us about yourself"))
        self.add_item(InputText(label="Favorite Roles", placeholder="e.g., Gamer, Artist", max_length=100))
        self.add_item(InputText(label="Social Media Links", placeholder="Add your social links", style=discord.InputTextStyle.long))

    async def on_submit(self, interaction: discord.Interaction):
        bio = self.children[0].value
        favorite_roles = self.children[1].value
        social_links = self.children[2].value

        # Store or update the profile in the database here (omitted for simplicity)
        
        await interaction.response.send_message(f"Profile setup complete! Here's a summary:\n\n**Bio:** {bio}\n**Favorite Roles:** {favorite_roles}\n**Social Media:** {social_links}", ephemeral=True)

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile_setup", description="Set up your profile.")
    async def profile_setup(self, interaction: discord.Interaction):
        await interaction.response.send_message("Let's get started with your profile setup!", ephemeral=True)
        await interaction.response.send_modal(ProfileSetupModal())

    @app_commands.command(name="profile_edit", description="Edit your profile.")
    async def profile_edit(self, interaction: discord.Interaction):
        # Assuming the profile details are fetched from the database
        # For now, we'll just open the setup modal again to edit details
        await interaction.response.send_message("Let's update your profile!", ephemeral=True)
        await interaction.response.send_modal(ProfileSetupModal())

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded!")

async def setup(bot):
    await bot.add_cog(ProfileCog(bot))
