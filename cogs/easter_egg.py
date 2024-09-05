import discord
import random

from discord.ext import commands
from discord.ui import Button, View

class easter_egg(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def siri(self,ctx):
        r = random.randint(1,6)
        if r == 1:
            await ctx.send("I’m not sure I understand.")
        elif r == 2:
            await ctx.send("Sorry, I didn’t quite get that.")
        elif r == 3:
            await ctx.send("Hmm, I’m having trouble with that.")
        elif r == 4:
            await ctx.send("Let me think... actually, I'm not sure.")
        elif r == 5:
            await ctx.send("I’m scratching my virtual head over here.")
        elif r == 6:
            await ctx.send("That sounds like a question for a human.")

    @commands.command()
    async def wert(self,ctx):
        await ctx.send( "### Still typing \"WHAT\"?  Pfft, that's so 2024.\n" +
                        "Welcome to the future: **\"WERT\"** is now the meta. "+
                        "Think about it—**\"wert\"** is a straight line on the keyboard. "+
                        "Imagine yourself as a keyboard virtuoso, fingers gliding like Mozart composing a masterpiece. "+
                        "**Boom!** \"WERT\" typed in **0.000001 seconds**. Efficiency at its finest.\n" +
                        "Truly the ultimate optimization of 2025. Don’t get left behind in the *what* stone age.")
    
    @commands.command()
    async def haka(self,ctx):
        await ctx.send("Haka, an expert of naming. Has created several original finding and gave them some interesting names. Here are a list of few:\n"+
                        "- Haka start(hgb)\n"+
                        "- No setup haka start(hgb)\n"+
                        "- wumimic start(hgb)\n"+
                        "- Imit-Leap start(hgb)\n"+
                        "- imitated jam start(hgb)\n"+
                        "- martial start(hgb)\n"+
                        "- haka jitter 0 cps\n"+
                        "- Haka bridge(honestly fine lol)\n"+
                        "- Hakawalk")
    

    @commands.command()
    async def poop(self,ctx):
        await ctx.send("I pooped here")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content == "fuck you":
            await message.channel.send("Bro you did that last night :skull: ")
        if message.content == "same" or message.content == "Same":
            await message.channel.send("same")

async def setup(bot):
    await bot.add_cog(easter_egg(bot))