import os
import asyncio
import discord
import cogs.lb
import cogs
from cogs.lb import pending_path,submisson_channel_id
from discord.ext import commands

secret_path = "data/secret.json"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"Logged in as --> {bot.user}")
    print("Bot is ready for dinner!")
    print(f"Loaded {len(slash)} slash command(s)")
    print("---------------------------")
    await cogs.lb.setup_hook(bot = bot)

@bot.command() 
@commands.is_owner()
async def sync(ctx): # oh yea let me sync the one and only one slash command
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} slash command(s).")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

@bot.command()
@commands.is_owner()
async def restart(ctx, silient = False):
    if silient:
        print("Restarting myself...")
    else:
        await ctx.send("Restarting myself...")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.reload_extension(f"cogs.{filename[:-3]}")
    if silient:
        print("Gg done!")
    else:
        await ctx.send("Gg done!")
    
@bot.command()
@commands.is_owner()
async def restartx(ctx):
    view = RestartButton(ctx)
    message = await ctx.send("Restart 0 times", view=view)
    view.message_id = message.id

@bot.command()
@commands.is_owner()
async def quit(ctx):
    await ctx.send("Good night ~~")  # but what if it was morning
    pending_dict = cogs.lb.load_json(pending_path)

    channel = bot.get_channel(submisson_channel_id)
    if channel:
        pending_dict.pop("counter")
        for pending_run in pending_dict.values():
            message_id = pending_run.get("Message id")
            if message_id:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.delete()
                except discord.NotFound:
                    print(f"Message {message_id} not found. It might have been deleted already.")
                except Exception as e:
                    print(f"Failed to delete message {message_id}: {e}")
    else:
        print("no such channel bru")

    await ctx.send("Zzzzzzz...")
    await bot.close()

class RestartButton(discord.ui.View):
    def __init__(self,ctx):
        super().__init__()
        self.counter = 0
        self.message_id = None
        self.ctx = ctx

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary)
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Ok", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have permission to use this button.", ephemeral=True)
            return
        self.counter += 1
        message = await self.ctx.fetch_message(self.message_id)
        await message.edit(content=f"Restart {self.counter} times", view = self)
        await restart(self.ctx, True)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        TOKEN = cogs.lb.load_json(secret_path)["Token"]
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
