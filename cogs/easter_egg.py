import datetime
import discord
import random

from discord.ext import commands

class easter_egg(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.response_cache = {}

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
        await ctx.send("Haka, an expert of naming. Let's see:\n"+
                        "- Haka start(hgb)\n"+
                        "- No setup haka start(hgb)\n"+
                        "- haka jitter 0 cps\n"+
                        "- Haka bridge\n"+
                        "- Hakawalk\n"+
                        "That's pretty interesting :thinking:")
    
    @commands.command()
    async def sigma(self, ctx, *, msg: str = ""):

        context = self.sigma_core(msg)
        if ctx.message.id in self.response_cache:
            bot_message = self.response_cache[ctx.message.id]
            await bot_message.edit(content = context)
        else:
            bot_message = await ctx.send(context)
            self.response_cache[ctx.message.id] = bot_message

    def sigma_core(self,msg: str):

        if msg == "":
            return "sigma can math"

        numbers = msg.split(" ")
        sum = 0
        try:
            for num in numbers:
                if "x" in num:
                    n = self.pie(num)
                else:
                    n = num
                sum += float(n)
        except:
            return "not sigma"

        if sum.is_integer():
            sum = int(sum)
        
        context = f"sigma is {sum}"
        
        return context

    def pie(self,msg: str):
        numbers = msg.split("x")
        product = 1
        try:
            for num in numbers:
                product *= float(num)
        except:
            raise ValueError
        return product

    @commands.command()
    async def curry(self,ctx):
        await ctx.send(":curry:", file = discord.File('data/curryeee.txt'))

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pinging the server...  please wait patiently")

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
    async def asian(self,ctx):
        responses = [
            "I'll send you to jesus",
            "Why do you have room temperature IQ",
            "Don't do drugs, they too expensive",
            "Rolex good for my wrist",
            "When I went to school, I walk 20 mile, uphill, both ways, 26 hours a day on 1 foot, my other foot was starting a business",
            "Stoooobid",
            "What da hail you say!",
            "START A BUN--?? I'M THE CEO OF BEIJING CORN!!",
            "When I was little, every morning I had to fight two lions",
            "Hallo, I am a professional Asian dad specializing in Failure Management.",
            "Ok, you will be a doctor.",
            "Don't be a dick!",
            "Can I have a discount?",
            "Want to know what B stand for? B stand for Stoopid!",
            "What da haail this? We're Asians, not Bsians!",
            "You have time to breathe, but not time to study? Failure!",
            "Timmy learned calculus from the back of milk cartons. Yet you still failure.",
            "Timmy learned to play Mozart from listening to the McDonalds jingle. Now he plays in his sleep.",
            "See your neighbor, he got 15 years work experience; he's 9!",
            "you look like a calculator"
        ]
        r = random.choice(responses)
        await ctx.send(r)

    @commands.command()
    async def todo(self,ctx):
        await ctx.send("to do list for Curryocity:\n"+
                       "- rest\n"+
                       "- sigmoid(enhance sigma)\n"+
                       "- wr\n"+
                       "- complete sentence\n"+
                       "- blacklist system\n"+
                       "- I made the !poll feature already btw, but the channel has to be setup by staff to use it\n"+
                       "- you could tell curry if you got interesting ideas\n"+
                       "- but curry is working on another project so likely he wouldn't update for a while\n"
                       )

    @commands.command()
    async def mute(self,ctx):
        duration = datetime.timedelta(seconds=60)
        try:
            user = ctx.message.author
            await user.timeout(duration)
        except Exception as e:
            print(e)
        await ctx.send("Sure, I'll mute you.")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content == "fuck you":
            await message.reply("Bro you did that last night :skull: ")
        if message.content == "same" or message.content == "Same":
            await message.channel.send("same")
        if message.content == "copycat":
            await message.channel.send("copycat")
        if "sigma" in message.content.lower() and not("!sigma" in message.content.lower()):
            await message.channel.send(f"ΣΣΣΣ ! <@{message.author.id}>!")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if after.content.startswith("!sigma"):
            new_ctx = await self.bot.get_context(after)
            await self.bot.invoke(new_ctx)

async def setup(bot):
    await bot.add_cog(easter_egg(bot))