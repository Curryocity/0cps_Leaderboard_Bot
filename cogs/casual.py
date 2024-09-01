import discord

from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from discord.ui import Select

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

    @app_commands.command(name = "intro", description = "Introducution of this bot")
    async def intro(self,interaction: discord.Interaction):
        await interaction.response.send_message("Hi, I am a bot designed to be the leaderboard manager of 0cps bridging community! \nStill work in progress :heart: ")

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
    await bot.add_cog(casual(bot))
