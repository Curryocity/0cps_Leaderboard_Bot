import discord

from discord.ext import commands
from discord.ui import Button, View

class easter_egg(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content == "fuck you":
            await message.channel.send("Bro you did that last night 💀 ")

async def setup(bot):
    await bot.add_cog(easter_egg(bot))