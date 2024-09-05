import discord

from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

class server(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name = "intro", description = "Introducution of this bot")
    async def intro(self,interaction: discord.Interaction):
        await interaction.response.send_message("Hi, I am a bot designed to be the leaderboard manager of 0cps bridging community! \nStill work in progress :heart:\n*(Hint: type !help to get started)*")

    @commands.command()
    async def help(self,ctx):
        await ctx.send("Still working on this part...\nCurrent advice: use !command to check all the commands")
    
    @commands.command(aliases=['commands'])
    async def command(self,ctx):
        await ctx.send("## list of commands (available for all members):\n"+
                       "**Server commands:**\n"+
                       "- help\n"+
                       "- command(s)\n"+
                       "- github\n"+
                       "**Leaderboard commands:**\n"+
                       "- lb\n"+
                       "- submit\n"+
                       "**Chat commands:** \n"+
                       "- click \n"+
                       "- cookie"+
                       "- needfriend\n"+
                       "- dice\n"+
                       "- why\n"+
                       "- joke\n"+
                       "- hello")

    @commands.command()
    async def github(self,ctx):
        await ctx.send(":blushed: You really want to see my inner source code?\n Sure! -> https://github.com/Curryocity/0cps_Leaderboard_Bot")

async def setup(bot):
    await bot.add_cog(server(bot))

