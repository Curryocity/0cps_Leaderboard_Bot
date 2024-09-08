import discord

from discord.ext import commands
from discord import app_commands

class server(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name = "intro", description = "Introducution of this bot")
    async def intro(self,interaction: discord.Interaction):
        await interaction.response.send_message("Hi, I am a bot designed to be the leaderboard manager of 0cps bridging community! \nStill work in progress :heart:\n*(Hint: type !help to get started)*")

    @commands.command()
    async def help(self,ctx):
        await ctx.send("Leaderboard section\nhttps://discord.com/channels/1224817276398735420/1281806474754130023 for announcement\n"+
                       "https://discord.com/channels/1224817276398735420/1281802864867414068 to get started\n"+
                       "https://discord.com/channels/1224817276398735420/1281802527221874688 ain't reading allat\n"+
                       "https://discord.com/channels/1224817276398735420/1281802906886209577 to learn useless informations\n"+
                       "https://discord.com/channels/1224817276398735420/1276982891531731070 if you got mental issues\n"+
                       "But who cares :nerd:\n"+
                       "**Most importantly, use '!command' to check out all of the commands**")
    
    @commands.command(aliases=['commands'])
    async def command(self,ctx):
        await ctx.send("## list of commands:\n"+
                       "**Server commands:**\n"+
                       "- help\n"+
                       "- command(s)\n"+
                       "- github\n"+
                       "- speedrun\n"+
                       "**Leaderboard commands:**\n"+
                       "- lb\n"+
                       "- submit\n"+
                       "- delete (Moderator or Admin only)\n"+
                       "- tie (Moderator or Admin only)\n"+
                       "**Chat commands:** \n"+
                       "- click\n"+
                       "- cookie\n"+
                       "- dice\n"+
                       "- hello\n"+
                       "- joke\n"+
                       "- music\n"+
                       "- needfriend\n"+
                       "***There is actually a lot more easter eggs not listed here hehe***")

    @commands.command()
    async def github(self,ctx):
        await ctx.send(":blushed: You really want to see my inner source code?\n Sure! -> https://github.com/Curryocity/0cps_Leaderboard_Bot")

    @commands.command()
    async def speedrun(self,ctx):
        await ctx.send("I am speeeeeeed ~~ :muscle: \nhttps://www.speedrun.com/0cps")

async def setup(bot):
    await bot.add_cog(server(bot))

