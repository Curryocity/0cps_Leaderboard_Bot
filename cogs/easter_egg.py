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
        await ctx.send("Haka, an expert of naming. Let's see:\n"+
                        "- Haka start(hgb)\n"+
                        "- No setup haka start(hgb)\n"+
                        "- haka jitter 0 cps\n"+
                        "- Haka bridge\n"+
                        "- Hakawalk"+
                        "That's pretty interesting :thinking:")
    
    @commands.command()
    async def sigma(self, ctx, *, msg: str = ""):

        numbers = msg.split(" ")
        sum = 0
        try:
            for num in numbers:
                sum += float(num)
        except:
            await ctx.send("not sigma")
            return

        if sum.is_integer():
            sum = int(sum)
        
        await ctx.send(f"sigma is {sum}")

    @commands.command()
    async def pi(self, ctx, *, msg: str = ""):

        numbers = msg.split(" ")
        product = 1
        try:
            for num in numbers:
                product *= float(num)
        except:
            await ctx.send("you might want a pie")
            return

        if product.is_integer():
            product = int(product)
        
        await ctx.send(f"sigma is {product}")
    
    @commands.command()
    async def pie(self,ctx):
        await ctx.send("π = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999...")

    @commands.command()
    async def e(self,ctx):
        await ctx.send("e = 2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274274663919320030599218174135966290435729003342952605956307381323286279434907632338298807531952510190115738341879307021540891499348841675092447614606680822648001684774118537423454424371075390777449920695517027618386062613313845830007520449338265602976067371132007093287091274437470472306969...")

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
            "I will send you to jesus",
            "Why do you have room temperature IQ",
            "Don't do drugs, they're too expensive",
            "Rolex good for my wrist",
            "When I went to school, I walk 20 mile, uphill, both ways, 26 hours a day on 1 foot, my other foot was starting a business",
            "Stoooobid",
            "What da hail you say!",
            "START A BUN--?? I'M THE CEO OF BEIJING CORN!!",
            "Every morning I had to fight two lions",
            "Hallo, I am a professional Asian dad specializing in Failure Management.",
            "You will be a doctor.",
            "Don't be a dick!",
            "Can I have a discount?",
            "Want to know what B stand for? B stand for Stoopid!",
            "What's this? We're Asians, not Bsians!",
            "You have time to breathe, but not time to study? Unbelievable!",
            "Timmy learned calculus from the back of milk cartons.",
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
                       "- blacklist system\n"
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
            await user.timeout(duration)
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
        if message.content == "copycat":
            await message.channel.send("copycat")
        if "sigma" in message.content.lower() and not("!sigma" in message.content.lower()):
            await message.channel.send(f"ΣΣΣΣ ! <@{message.author.id}>!")
        if "nigger" in message.content.lower() and not("snigger" in message.content.lower()):
            user = message.author
            duration = datetime.timedelta(seconds=300)
            await user.timeout(duration)
            await message.channel.send(f"N word detected, <@{message.author.id}> wert a shame!")

async def setup(bot):
    await bot.add_cog(easter_egg(bot))