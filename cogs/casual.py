import discord
import random

from .lb import load_json
from discord.ext import commands
from discord.ui import Button, View


secret_path = "data/secret.json"
poll_channel_id = load_json(secret_path)["Poll Channel id"]

class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.button = Button(label="Press Me", style=discord.ButtonStyle.blurple)
        self.button.press_count = 0

        async def button_callback(interaction: discord.Interaction):
            self.button.press_count += 1
            self.button.label = f"Pressed {self.button.press_count} times"
            await interaction.response.edit_message(content=f"Button pressed {self.button.press_count} times", view=self)
            if self.button.press_count == 69:
                await interaction.followup.send("Noice~")
            

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
    @commands.is_owner()
    async def say(self, ctx, *, msg: str):
        if ctx.message.reference:  
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await replied_message.reply(msg)
        else:
            await ctx.send(msg)
        await ctx.message.delete()
        

    @commands.command()
    @commands.is_owner()
    async def edit(self, ctx, *, msg: str = ""):
        if ctx.message.reference:  
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if replied_message.author == self.bot.user:
                if msg == "":
                    await replied_message.delete()
                else:
                    await replied_message.edit(content = msg)
        await ctx.message.delete()

    @commands.command()
    async def embed(self, ctx, *, args: str = ""):
        if args == "":
            await ctx.send("## !embed <content> <,, title: optional>\n")
            return
        if ",," in args:
            parts = args.split(",,", 1)
            content = parts[0].strip()
            title = parts[1].strip()
            if title == "":
                await ctx.reply("Don't type **,,** if you are not entering the title")
                return
        else:
            title = None
            content = args.strip()

        embed = discord.Embed(title = title, description = content, color= 0xa800e6)
        embed.set_author(name= f"{ctx.author}#{ctx.author.discriminator}", icon_url = ctx.author.avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    @commands.command()
    async def click(self,ctx):
        view = ButtonView()
        await ctx.send("here is your button:", view=view)

    @commands.command()
    async def needfriend(self,ctx):
        view = ModalButton()
        await ctx.send("need someone to talk to you?",view = view)

    @commands.command()
    async def cookie(self,ctx):
        await ctx.send("wtf that's my cookie!\ngo away!")

    @commands.command()
    async def hello(self,ctx):
        response = [
        "*The room falls eerily quiet...*\n"
        "*A faint breeze drifts by, carrying nothing but the sound of distant silence.*\n"
        "*Even the crickets refuse to break the stillness. It's as if the very world holds its breath, waiting... but no reply comes.*"
        ,
        "*You shout into the void...*\n"
        "*The sound echoes endlessly, bouncing off unseen walls of an infinite expanse.*\n"
        "*Time itself seems to slow, each second dragging on for what feels like an eternity.*\n"
        "*No birds chirp. No winds howl. Even the pixels on your screen seem to hesitate.*\n"
        "*The universe pauses, as if contemplating whether to respond... but no one answers.*\n"
        "*It’s just you... alone... with your thoughts.*"
        ,
        "*You call out...*\n"
        "*The silence stretches on, deep and unbroken.*\n"
        "*Not even a whisper of wind or the faintest rustle of leaves responds.*\n"
        "*The world holds its breath, waiting... but no reply comes.*\n"
        "*It’s just you, standing there, in a vast and empty silence.*"
        ,
         "*You speak, your words drifting into the air...*\n"
        "*The quiet is deafening, as if the universe itself forgot how to respond.*\n"
        "*No echo, no reaction — only the weight of your own presence in the void.*\n"
        "*It's as though the world simply doesn’t care to acknowledge your call.*"
        ,
        "*You shout, but the sound is swallowed instantly.*\n"
        "*Not a creature stirs, not a soul moves.*\n"
        "*The stillness is oppressive, like time itself has stopped just to ignore you.*\n"
        "*You wait... and wait... but the silence never ends.*"
        ]
        r = random.choice(response)
        await ctx.send(r)

    @commands.command()
    async def dice(self,ctx):
        num = random.randint(1,6)
        await ctx.send(f"u got {num}")

    @commands.command()
    async def music(self,ctx):
        await ctx.send("Absolutely recommend this banger :fire: : [https//www.youtube.com/watch?v=ZHFgk8Eo0FE](<https://www.youtube.com/watch?v=dQw4w9WgXcQ>)")

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
            "Did you hear about the gardener who was excited for spring? She wet her plants.",
            "Q: What did the triangle say to the circle?\nA: You’re pointless.",
            "RIP, boiling water. You will be mist.",
            "Time flies like an arrow. Fruit flies like a banana.",
            "I ordered a chicken and an egg online. I’ll let you know what comes first.",
            "Q: What did one toilet say to another?\nA: You look flushed.",
            "Q: What does a baby computer call his father?\nA: Data!",
            "Q: What kind of tea is hard to swallow?\nA: Realitea!",
            "Q: Why do French people eat snails?\nA: They don’t like fast food."
        ]
        j = random.choice(jokes)
        await ctx.send(j)

    @commands.command()
    async def poll(self,ctx, *, args: str = ""):

        if args == "":
            await ctx.send("## Syntax: !poll <question> ,, <emojis:optional>\n"+
                           "1. **,,** is the seperator of question and emoji\n"+
                           "2. You don't have to type emoji if you want the default ones\n"+
                           "3. Don't use **,,** for non-seperator or you might send a broken message\n"+
                           "ex. !poll Do you want to marry me? ,, :white_check_mark: :x: :middle_finger:")
            return
        if ",," in args:
            parts = args.split(",,", 1)
            question = parts[0].strip()
            emojis = parts[1].replace(" ", "")
            if emojis == "":
                await ctx.reply("Don't type **,,** if you don't enter emojis")
                return
        else:
            emojis = None
            question = args.strip()

        embed = discord.Embed(title="poll",description = question, color= 0xa800e6)
        embed.set_author(name= f"{ctx.author}#{ctx.author.discriminator}", icon_url = ctx.author.avatar.url)
        channel = self.bot.get_channel(poll_channel_id)
        if channel:
            try:
                poll_message = await channel.send(embed=embed)

                if emojis is None:
                    await poll_message.add_reaction('⬆️')
                    await poll_message.add_reaction('⬇️')
                    await poll_message.add_reaction('↕️')
                else:
                    emoji_counter = 0
                    for emoji in emojis:
                        try:
                            await poll_message.add_reaction(emoji)
                            emoji_counter += 1
                        except discord.HTTPException:
                            continue
                    if emoji_counter < 2:
                        await poll_message.delete()
                        await ctx.reply("You are not giving enough options, need at least 2")
                        return

                await ctx.reply("Greenfully made poll!")
            except Exception as e:
                print(e)
                await poll_message.delete()
                await ctx.reply("An error occured")
        else:
            await ctx.reply("error: poll channel wasn't setupped")

async def setup(bot):
    await bot.add_cog(casual(bot))
