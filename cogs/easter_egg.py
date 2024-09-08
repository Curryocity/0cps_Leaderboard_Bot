import datetime
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
            await ctx.send("Hmm, I’m having trouble talking with you.")
        elif r == 4:
            await ctx.send("Let me think... actually, I don't care.")
        elif r == 5:
            await ctx.send("I’m scratching my virtual head over here.")
        elif r == 6:
            await ctx.send("Well, that sounds like a question for human.")

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

    @commands.command()
    async def update(self,ctx):
        await ctx.send("update your retarded brain first")

    @commands.command()
    async def why(self,ctx):
        r = random.randint(0,1)
        if r == 0:
            await ctx.send("why not?")
        else:
            await ctx.send("because yes")       

    @commands.command()
    async def idea(self,ctx):
        await ctx.send("such as removing you from the server")

    @commands.command()
    async def chatgpt(self,ctx):
        await ctx.send("do I look like a chatgpt? :middle_finger:")

    @commands.command()
    async def todo(self,ctx):
        await ctx.send("to do list for Curryocity:\n"+
                       "- better todo command\n"+
                       "- poll\n"+
                       "- efficient code\n"
                       "- more server commands\n"
                       )
        
    @commands.command()
    async def useless(self,ctx):
        await ctx.send("If you think you're useless, look at these:\n"+
                       "https://discord.com/channels/1224817276398735420/1237070688146292866 https://discord.com/channels/1224817276398735420/1237070847676780564\n"+
                       "https://discord.com/channels/1224817276398735420/1237304439212343348 https://discord.com/channels/1224817276398735420/1237304488885358623\n"+
                       "https://discord.com/channels/1224817276398735420/1237070654935793816 https://discord.com/channels/1224817276398735420/1237070807218524291\n"+
                       ": D"
                       )

    @commands.command()
    async def mute(self,ctx):
        duration = datetime.timedelta(seconds=60)
        try:
            user = ctx.message.author
            await user.timeout(duration, reason = "funny")
        except Exception as e:
            print(e)
        await ctx.send("Sure, I'll mute you.")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content == "fuck you":
            await message.channel.send("Bro you did that last night :skull: ")
        if message.content == "same" or message.content == "Same":
            await message.channel.send("same")
        if message.content == "ello":
            await message.channel.send("ello")
        if message.content == "copycat":
            await message.channel.send("copycat")
        if "nigger" in message.content.lower() and not("snigger" in message.content.lower()):
            await message.channel.send(f"N word detected, <@{message.author.id}> wert a shame!")

async def setup(bot):
    await bot.add_cog(easter_egg(bot))