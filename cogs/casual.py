import discord
import random

from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.button = Button(label="Press Me", style=discord.ButtonStyle.blurple)
        self.button.press_count = 0

        async def button_callback(interaction: discord.Interaction):
            self.button.press_count += 1
            self.button.label = f"Pressed {self.button.press_count} times"
            await interaction.response.edit_message(content=f"Button pressed {self.button.press_count} times", view=self)

        self.button.callback = button_callback

        self.add_item(self.button)

class ModalClass(discord.ui.Modal, title = "I wanted to know more about you"):

    age = discord.ui.TextInput(label= "age", placeholder="casual question I know")
    food = discord.ui.TextInput(label = "favorite food", placeholder="a coincidence is gonna happen")
    
    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        await interaction.response.send_message(f"Hello, <@{user_id}> !\nI am also {self.age.value} years old, and my favorite food is {self.food.value}, too. What a coincidence!")

class ModalButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.button= Button(label="Apply for 'Hi'", style=discord.ButtonStyle.green)

        async def button_callback(interaction: discord.Interaction):
            modal = ModalClass()
            await interaction.response.send_modal(modal)

        self.button.callback = button_callback
        self.add_item(self.button)

class casual(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def click(self,ctx):
        view = ButtonView()
        await ctx.send("Here is your button:", view=view)

    @commands.command()
    async def needfriend(self,ctx):
        view = ModalButton()
        await ctx.send("need someone to talk to you?",view = view)

    @commands.command()
    async def poop(self,ctx):
        await ctx.send("I pooped here")

    @commands.command()
    async def dice(self,ctx):
        num = random.randint(1,6)
        await ctx.send(f"u got {num}")

    @commands.command()
    async def why(self,ctx):
        r = random.randint(0,1)
        if r == 0:
            await ctx.send("why not?")
        else:
            await ctx.send("because yes")

    @commands.command()
    async def joke(self,ctx):
        jokes = [
            "Q: Why did the scarecrow win an award?\nA: Because he was outstanding in his field!",
            "Q: Why don’t scientists trust atoms?\nA: Because they make up everything!",
            "Q: What do you call fake spaghetti?\nA: An impasta!",
            "Q: Why did the bicycle fall over?\nA: Because it was two-tired!",
            "Q: How does a penguin build its house?\nA: Igloos it together.",
            "Q: What did the grape do when it got stepped on?\nA: Nothing, it just let out a little wine.",
            "Q: Why don’t oysters share their pearls?\nA: Because they’re shellfish.",
            "Q: Why did the math book look sad?\nA: Because it had too many problems.",
            "Q: Why don’t eggs tell jokes?\nA: They’d crack each other up!",
            "Q: How do you organize a space party?\nA: You planet!",
            "Q: What did one wall say to the other?\nA: I’ll meet you at the corner!",
            "Q: Why don’t some couples go to the gym?\nA: Because some relationships don’t work out!",
            "Q: What do you call a factory that makes okay products?\nA: A satisfactory.",
            "Q: How does a cucumber become a pickle?\nA: It goes through a jarring experience!",
            "Q: Why was the tomato blushing?\nA: Because it saw the salad dressing!",
            "Q: What did the fish say when it hit the wall?\nA: Dam!",
            "Q: What do you call an alligator in a vest?\nA: An investigator. And if you ask it about your missing socks, it might just be on the case!",
            "Two fish are in a tank. One turns to the other and says, 'Any idea how to drive this thing?'",
            "Q: Why did the invisible man quit his job?\nA: He couldn't see himself doing it.",
            "Did you hear about the pine tree that got a timeout? It was being knotty.",
            "I met a giant once. I didn't know what to say, so I just used big words.",
            "I'd tell you a construction joke, but I'm still working on it.",
            "Q: How did police catch the thief who robbed an Apple store?\nA: There was an iWitness.",
            "I'm obsessed with telling airport jokes. My doctor says it's a terminal problem.",
            "I was going to tell you a joke about sodium, but then I thought, 'Na.'",
            "Did you hear about the gardener who was excited for spring? She wet her plants."
        ]
        j = random.choice(jokes)
        await ctx.send(j)

    @commands.command()
    async def hello(self,ctx):
        await ctx.send("shut the fuck up no one cares about you")


async def setup(bot):
    await bot.add_cog(casual(bot))
