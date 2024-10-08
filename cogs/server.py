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
        await ctx.send("Check out\n"+
                       "https://discord.com/channels/1224817276398735420/1237071501073580114 server rule (not copypasta)\n"+
                       "https://discord.com/channels/1224817276398735420/1281802527221874688 to get started\n"+
                       "https://discord.com/channels/1224817276398735420/1281802906886209577 ain't reading allat\n"+
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
                       "- delete & tie (Moderator or Admin only)\n"+
                       "**Misc commands:**\n"+
                       "- click, cookie, dice, embed, hello, joke, music, needfriend\n"+
                       "***There is actually a lot more easter eggs not listed here hehe***")

    @commands.command()
    async def github(self,ctx):
        await ctx.send("You really want to see my source code? :blushed:\n Sure! -> https://github.com/Curryocity/0cps_Leaderboard_Bot")

    @commands.command()
    async def speedrun(self,ctx):
        await ctx.send("I am speeeeeeed ~~ :muscle: \nhttps://www.speedrun.com/0cps")

async def setup(bot):
    await bot.add_cog(server(bot))

