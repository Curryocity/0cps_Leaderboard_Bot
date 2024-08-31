import discord

from discord.ext import commands
from discord import app_commands
from typing import Optional
from discord.app_commands import Choice
from discord.ui import Button, View
from discord.ui import Select

class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.button = Button(label="Press Me", style=discord.ButtonStyle.blurple)
        self.button.press_count = 0

        # Define the callback function for the button
        async def button_callback(interaction: discord.Interaction):
            self.button.press_count += 1
            self.button.label = f"Pressed {self.button.press_count} times"
            await interaction.response.edit_message(content=f"Button pressed {self.button.press_count} times", view=self)

        # Attach the callback to the button
        self.button.callback = button_callback

        # Add the button to the view
        self.add_item(self.button)

class SelectMenu(View):
    @discord.ui.select(
        placeholder= "What do you want to buy",
        options = [discord.SelectOption(label="Hamburger",value= 0, description="triple cheese!"),
                   discord.SelectOption(label="Pizza",value= 1, description="with pineapple"),
                   discord.SelectOption(label="Poop",value= 2, description="Yumm, pure gold")
                   ]
    )

    async def select_callback(self,interaction:discord.Interaction ,select: Select):
        price = 0
        name = ""
        value = select.values[0]
        if value == "0":
            price = 520
            name = "Hamburger"
        if value == "1":
            price = 314
            name = "Pizza"
        if value == "2":
            price = 99999
            name = "Poop"
        await interaction.response.edit_message(content= f"You bought {name}, it is {price} dollars.")

class ModalClass(discord.ui.Modal, title = "What should I call you?"):

    name = discord.ui.TextInput(label = "Name",required=True)
    age = discord.ui.TextInput(label= "age", placeholder="a miracle is gonna happen")


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {self.name.value}! \nI am also {self.age.value} years old, what a coincidence!")

class ModalButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.button= Button(label="Apply for 'Hi'", style=discord.ButtonStyle.green)

        async def button_callback(interaction: discord.Interaction):
            modal = ModalClass()
            await interaction.response.send_modal(modal)

        self.button.callback = button_callback
        self.add_item(self.button)



class command(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name = "intro", description = "Introducution of this bot")
    async def intro(self,interaction: discord.Interaction):
        await interaction.response.send_message("Hi, I am a bot designed to be the leaderboard manager of 0cps bridging community! \nStill work in progress :heart: ")
    
    @app_commands.command(name = "add", description = "The only math that a 3yr old kid can do")
    @app_commands.describe(a = "integer", b = "integer" , humble = "be humble?")
    @app_commands.choices(
        humble = [Choice(name = "YES", value = 1), Choice(name = "NO", value = 0 )]
    )
    async def add(self,interaction: discord.Interaction,  humble: Choice[int], a:Optional[int] = None, b:Optional[int] = None):
        humble = humble.value
        if a==None:
            a=1
        if b==None:
            b=1
        if humble == 0:
            await interaction.response.send_message(f"{a} + {b} = {a+b} , I'm just too smart")
        if humble == 1:
            await interaction.response.send_message(f"{a} + {b} = {a+b} , shit I cannot brag cus I'm suppose to be humble :sunglasses:")


    @commands.command()
    async def click(self,ctx):
        view = ButtonView()
        await ctx.send("Here is your button:", view=view)

    @commands.command()
    async def buy(self,ctx):
        view = SelectMenu()
        await ctx.send("Here's the menu:", view = view)

    @commands.command()
    async def needfriend(self,ctx):
        view = ModalButton()
        await ctx.send("need someone to talk to you?",view = view)

    @commands.command()
    async def msg(self,ctx,user: discord.Member,message):
        await user.send(message)
        await ctx.send(f"successfully send to @{user}")

    @commands.command()
    async def poop(self,ctx):
        await ctx.send("I pooped here")

    @commands.command()
    async def hello(self,ctx):
        await ctx.send("shut the fuck up no one cares about you")


    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content == "fuck you":
            await message.channel.send("Bro you did that last night 💀 ")

async def setup(bot):
    await bot.add_cog(command(bot))
