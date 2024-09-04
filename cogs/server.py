import discord

from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

class server(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name = "intro", description = "Introducution of this bot")
    async def intro(self,interaction: discord.Interaction):
        await interaction.response.send_message("Hi, I am a bot designed to be the leaderboard manager of 0cps bridging community! \nStill work in progress :heart: ")

async def setup(bot):
    await bot.add_cog(server(bot))

