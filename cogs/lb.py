import discord
import json
import os
import re
import traceback

from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from discord.ui import Select

submisson_channel_id = 1277915107829223538
pending_path = "data/pending.json"
leaderboard_path = "data/leaderboard.json"
obsolete_path = "data/obsolete.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)
    else:
        print(f"{path} not found")
    return {}

def save_json(path , dict):
    with open(path, 'w') as file:
        json.dump(dict, file, indent=4)

leaderboard_dict = load_json(leaderboard_path)
obsolete_dict = load_json(obsolete_path)
pending_dict = load_json(pending_path)
pending_id = pending_dict.get("counter", None)
if pending_id is None:
    pending_id = 0
    pending_dict["counter"] = None
    save_json(pending_path, pending_dict)
    print("Error: 'counter' in pending.json is missing, please fix it as soon as possible.")

async def setup_hook(bot):
    print("Setup_hook...", end = ' ')
    try:
        pending_runs = load_json(pending_path)
        pending_runs.pop("counter")
        for i,pending_run in pending_runs.items():
            
            if "Distance" in pending_run["Category"]:
                value = pending_run["Distance"]
                tellyq = None
            else:
                value = pending_run["Time"]
                tellyq = pending_run["Telly?"]

            await send_submission(bot = bot, run_id = i, value = value, tellyq = tellyq, newq = False)
        print("Done")
    except Exception as e:
        print(e)

class lb(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def lb(self,ctx):
        await ctx.send("Select a category:", view = InitialButton(tag = "lb"))

    @commands.command()
    async def submit(self,ctx):
        await ctx.send("[**Mode: Submit**] Select a category:", view = InitialButton(tag = "submit"))

    @commands.command()
    @commands.is_owner()
    async def delete(self, ctx, param = "", runner_id = None):
        if param == "":
            await ctx.send("## Need Help? \n ## Syntax: !delete <category tag> <runner_id>\n"+
                           "1. **m**:  McPlayHD,  **b**:  BridgerLand,  **d**:  Distance\n"+
                           "2. **Digit** for sub-category. Start from 1, 'weak' to 'strong', then incline (should be intuitive)\n"+
                           "3. **y/n** correspond to telly and tellyless (leave it blank if None)\n"+
                           "e.g.  ***!delete m2n ..***  means delete run from \"McPlayHD Short Tellyless%\"\n"+
                           "        ***!delete d4  ..***  means delete run from \"Distance Hold Diag Fruit\"")
        else:
            param = param.lower()
            tellyq = None
            if param.endswith("y"):
                tellyq = True
                param = param.removesuffix("y")
            elif param.endswith("n"):
                tellyq = False
                param = param.removesuffix("n")
            tellyreq = ["m1","m2","m3","m4","b1","b2"]
            category_map = {"m1":"McPlayHD Extra Short", "m2":"McPlayHD Short", "m3":"McPlayHD Normal", "m4":"McPlayHD Long", "m5":"McPlayHD Inclined Short", "m6":"McPlayHD Inclined Normal", 
                            "b1":"BridgerLand Short", "b2":"BridgerLand Regular", "b3":"BridgerLand Inclined",
                            "d1":"Distance Cha Cha", "d2":"Distance HGB","d3":"Distance Dao Telly","d4":"Distance Hold Diag Fruit"}
            if param in category_map:
                category = category_map[param]
                confirm_msg = f"{category}"
                if (param in tellyreq) ^ (tellyq is None):
                    if tellyq is True:
                        confirm_msg += " Telly%"
                    elif tellyq is False:
                        confirm_msg += " Tellyless%"
                else:
                    await ctx.send("Invalid telly tag, !delete to check out the guide.")
                    return
                if runner_id is None:
                    await ctx.send("Runner id?")
                    return

                runner_name = await get_user_name(self.bot, runner_id, f"I don't think there is runner with id  '{runner_id}'", ctx)
                if runner_name is None:
                    return
                
                templb = load_json(leaderboard_path).get(category,None)
                if templb is None:
                    await ctx.send(f"{runner_name} does not have a run in {confirm_msg}")
                    return

                for i, run in enumerate(templb):
                    if run["Runner id"] == int(runner_id):
                        if tellyq is run.get("Telly?", None):
                            confirm_msg = f"Are you sure to delete {runner_name}'s run in {confirm_msg} ?"
                            await ctx.send(confirm_msg, view = DeleteButton(category = category, index = i))
                            return

                await ctx.send(f"{runner_name} does not have a run in {confirm_msg}")
            else:
                await ctx.send("Invalid category tag, !delete to check out the guide.")

    @commands.command()
    @commands.is_owner()
    async def clear_pending(self,ctx):
        global pending_dict
        global pending_id
        pending_id = 0
        pending_dict = {"counter":pending_id}
        save_json(pending_path,pending_dict)
        await ctx.send("Oops I might have cleared the entire pending.json lo/")

    @commands.command()
    @commands.is_owner()
    async def traceback(self,ctx):
        traceback.print_stack()
        await ctx.send("printed traceback to console")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data["custom_id"]
            tag = custom_id.split('+')[-1]

            if custom_id.startswith("_"):

                category = ((custom_id.lstrip("_")).removesuffix(f"+{tag}")).replace("_"," ")

                if tag == "submit":
                    modal = SubmitGUI(category= category, submitter_id= interaction.user.id, bot= self.bot)
                    await interaction.response.send_modal(modal)
                elif tag == "lb":
                    content = self.generatelb(category = category)
                    await interaction.response.edit_message(content = content)
                    
            elif "McPlayHD" in custom_id:
                names = [
                    "Extra Short", "Short", "Normal", "Long", 
                    "Inclined Short", "Inclined Normal"
                ]
                buttons = [
                    Button(label=name, style=discord.ButtonStyle.blurple, custom_id=f"_McPlayHD_{name.replace(' ','_')}+{tag}")
                    for name in names
                ]
                buttons.append(Button(label="<--", style=discord.ButtonStyle.red, custom_id=f"goBack+{tag}"))
                view = View()
                for button in buttons:
                    view.add_item(button)

                content = "Select a sub-category for McPlayHD:"
                if tag == "submit":
                    content = f"[**Mode: Submit**] {content}"
                await interaction.response.edit_message(content=content, view=view, embed=None)
        
            elif "BridgerLand" in custom_id:
                names = [
                    "Short","Regular","Inclined"
                ]
                buttons = [
                    Button(label=name, style=discord.ButtonStyle.blurple, custom_id=f"_BridgerLand_{name.replace(' ','_')}+{tag}")
                    for name in names
                ]
                buttons.append(Button(label="<--", style=discord.ButtonStyle.red, custom_id=f"goBack+{tag}"))
                view = View()
                for button in buttons:
                    view.add_item(button)
                
                content = "Select a sub-category for BridgerLand:"
                if tag == "submit":
                    content = f"[**Mode: Submit**] {content}"
                await interaction.response.edit_message(content=content, view=view, embed=None)

            elif "Distance" in custom_id:
                names = [
                    "Cha Cha","HGB","Dao Telly","Hold Diag Fruit"
                ]
                buttons = [
                    Button(label=name, style=discord.ButtonStyle.green, custom_id=f"_Distance_{name.replace(' ','_')}+{tag}")
                    for name in names
                ]
                buttons.append(Button(label="<--", style=discord.ButtonStyle.red, custom_id=f"goBack+{tag}"))
                view = View()
                for button in buttons:
                    view.add_item(button)
                
                content = "Select a sub-category for Distance:"
                if tag == "submit":
                    content = f"[**Mode: Submit**] {content}"
                await interaction.response.edit_message(content=content, view=view, embed=None)

            elif "goBack" in custom_id:
                names = [
                    "McPlayHD","BridgerLand","Distance"
                ]
                buttons = [
                    Button(label=name, style=discord.ButtonStyle.blurple if name != "Distance" else discord.ButtonStyle.green,
                            custom_id=f"{name.replace(' ','_')}+{tag}")
                    for name in names
                ]
                view = View()
                for button in buttons:
                    view.add_item(button)
                content = "Select a category:"
                if tag == "submit":
                    content = f"[**Mode: Submit**] {content}"
                await interaction.response.edit_message(content=content, view=view, embed=None)

    def generatelb(self, category):
        content = ""
        tempLB = load_json(leaderboard_path).get(category, [])
        if not tempLB:
            content = f"There's no runs in **{category}** :sob:"
        else:
            tellyless_exist = False
            content = f"The Leaderboard for **{category}**: \n"
            if "Distance" in category:
                for i, run in enumerate(tempLB):
                    content += f"{i+1}. {run['Runner name']}:  [{run['Distance']}b](<{run['Link']}>)\n"
            else:
                for i, run in enumerate(tempLB):
                    if run["Telly?"] is False:
                        content += f"{i+1}. :sloth: {run['Runner name']}:  [{run['Time']}s](<{run['Link']}>)\n"
                        tellyless_exist = True
                    else:
                        content += f"{i+1}. {run['Runner name']}:  [{run['Time']}s](<{run['Link']}>)\n"
            if tellyless_exist: content += ("(:sloth: --> the run is performed ***tellyless***)")

        return content

class SubmitGUI(Modal, title = "Submit your run"):
    def __init__(self, bot, category, submitter_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.category = category
        self.submitter_id = submitter_id
        self.submitter_name = None
        self.runner_id = self.submitter_id
        self.runner_name = None

        if "Distance" in self.category:
            self.add_item(TextInput(label="Distance", placeholder="Unit: block(s)"))
        else:
            self.add_item(TextInput(label="Time", placeholder="Unit: second(s)"))
            if not("Inclined" in self.category):
                self.add_item(TextInput(label="Sprint restriction?", placeholder="'0' if telly%, '1' if tellyless%"))
        self.add_item(TextInput(label= "Video Link", placeholder="Paste a permanent & direct link"))
        self.add_item(TextInput(label = "Runner id", placeholder="Leave it blank if you're the runner", required= False))

    async def on_submit(self, interaction: discord.Interaction):
        global pending_id
        self.submitter_name = await get_user_name(self.bot, self.submitter_id)
        self.runner_name = self.submitter_name
        value = self.children[0].value

        tellyq = None
        if not(("Distance" in self.category) or ("Inclined" in self.category)):
            if self.children[1].value == "0":
                tellyq = True
            elif self.children[1].value == "1":
                tellyq = False
            else:
                await interaction.response.send_message(f"You should only put 0 or 1 in the 'Rescriction mode', read the rule for further info.")
                return
            
        link = self.children[-2].value
        if not(is_link(link)):
            await interaction.response.send_message(f"(Probably) invalid link")
            return
        
        if self.children[-1].value != "":
            try:
                self.runner_id = self.children[-1].value
                self.runner_name = await get_user_name(self.bot, self.runner_id)
            except Exception as e:
                await interaction.response.send_message(f"I cun't fetch runner id, plz chuck if the id were valid.")
                return
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
            
            if "Distance" in self.category:
                if not(value.is_integer()):
                    raise ValueError
                value = int(value)
                pending_dict[pending_id] = {"Runner name":self.runner_name,"Runner id":self.runner_id,"Category":self.category,"Distance": value,"Link":link,"Submitter name": self.submitter_name,"Submitter id":self.submitter_id} 
            else:
                if abs(value/0.05-round(value/0.05)) < 0.0000001 :
                    pending_dict[pending_id] = {"Runner name":self.runner_name,"Runner id":self.runner_id,"Category":self.category,"Time": value,"Telly?":tellyq,"Link":link,"Submitter name": self.submitter_name,"Submitter id":self.submitter_id} 
                else:
                    await interaction.response.send_message(f"Minecraft runs on tick(0.05s) dummy, do you think {value}s is reasonable?")
                    return
            
            save_json(pending_path,pending_dict)
            await send_submission(bot = self.bot, run_id = pending_id, value = value, tellyq = tellyq)
            await interaction.response.send_message(f"You have greenfully submitted, id:{pending_id - 1}")

        except ValueError:
            await interaction.response.send_message(f"Bro what the gibberish are you trying to submit!")
        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.response.send_message(f"Uh it failed, idk why (I am very responsible)")

class VerificationView(View):
    def __init__(self, run_id, bot):
        super().__init__(timeout = None)
        self.run_id = run_id
        self.bot = bot
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        submission = pending_dict.pop(self.run_id, None)
        if submission:
            self.insertLB(submission["Category"], submission)
            save_json(pending_path , pending_dict)
            save_json(leaderboard_path, leaderboard_dict)
            save_json(obsolete_path, obsolete_dict)
            await interaction.response.send_message(f'The run for {submission["Runner name"]} in category **{submission["Category"]}** has been verified and added to the leaderboard.', ephemeral=True)
            
            await dm_user(self.bot, submission["Runner id"], f"Your submission for the category **{submission['Category']}** has been verified and added to the leaderboard.")
            channel = self.bot.get_channel(submisson_channel_id)
            
            if channel:
                message = await channel.fetch_message(submission["Message id"])
                await message.edit(content= message.content.replace("**Pending** :thinking:", "**Verified** :white_check_mark:"), view=None)
        else:
            await interaction.response.send_message('The submission could not be found.', ephemeral=True)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RejectionGUI(run_id = self.run_id, bot = self.bot))

    def insertLB(self, category, submission, obsoleteq = False):
        target_dict = leaderboard_dict
        if obsoleteq:
            target_dict = obsolete_dict

        if category not in target_dict:
            target_dict[category] = []
        if "Time" in submission:
            thisrun = {"Runner name":submission["Runner name"], "Runner id":submission["Runner id"], "Time":submission["Time"], "Telly?":submission["Telly?"], "Link":submission["Link"]}
            focus, flipq = "Time", True
        else:
            thisrun = {"Runner name":submission["Runner name"], "Runner id":submission["Runner id"], "Distance":submission["Distance"], "Link":submission["Link"]}
            focus, flipq = "Distance", False
        
        focus_value = thisrun[focus]
        for i, run in enumerate(target_dict[category]):
            if ((focus_value > run[focus]) ^ flipq) and focus_value != run[focus]:
                target_dict[category].insert(i, thisrun)
                if not(obsoleteq): 
                    self.moveObsolete(submission["Runner id"], category)
                return
        target_dict[category].append(thisrun)
        if not(obsoleteq): 
            self.moveObsolete(submission["Runner id"], category)
    
    def moveObsolete(self, runner_id, category):
        obsoleteRuns = []
        updatedLB = []
        tags = []
        for i, run in enumerate(leaderboard_dict[category]):
            if ((run["Runner id"]) == runner_id):
                tellyq = run.get("Telly?", None)
                if not(tags):
                    if tellyq is None:
                        tags = ["full"]
                    else:
                        tags = [tellyq]
                    updatedLB.append(leaderboard_dict[category][i])
                else:
                    if (tellyq in tags) or ("full" in tags):
                        obsoleteRuns.append(leaderboard_dict[category][i])
                    else:
                        if not(tellyq is None): tags.append(tellyq)
                        updatedLB.append(leaderboard_dict[category][i])
            else:
                updatedLB.append(leaderboard_dict[category][i])
        leaderboard_dict[category] = updatedLB
        for run in obsoleteRuns:
            self.insertLB(category, run, True)

class RejectionGUI(Modal):
    def __init__(self, run_id, bot, *args, **kwargs):
        super().__init__(title="Rejection Reason", *args, **kwargs)
        self.run_id = run_id
        self.bot = bot
        self.add_item(TextInput(label="Reason", placeholder="Why do you reject the run?"))
        

    async def on_submit(self, interaction: discord.Interaction):
        reason = self.children[0].value
        self.submission = pending_dict.pop(self.run_id, None)
        try:
            if self.submission:
                await dm_user(self.bot, self.submission["Runner id"],f"Fortunately, your submission to the {self.submission['Category']} leaderboards has been rejected for the reason: ***{reason}***.\n~~*(Feel free to cry if you believe this is wrong or unjustified)*~~")
                channel = self.bot.get_channel(submisson_channel_id)
                if channel:
                    message = await channel.fetch_message(self.submission["Message id"])
                    await message.edit(content=message.content.replace("**Pending** :thinking:", f"**Rejected** :x:\n**Reason: {reason}**"), view=None)
                save_json(pending_path, pending_dict)
            else:
                print(f"submission {self.run_id} not found")
            await interaction.response.send_message('The submission has been rejected and the runner has been notified.', ephemeral=True)
        except Exception as e:
            pending_dict.append(self.submission)
            await interaction.response.send_message(f"Error msg: {e}\nPlease try again, it should be working fine. Hope it is Discord's issue", ephemeral=True)

class InitialButton(View):
    def __init__(self, tag : str, selected = 0):
        super().__init__(timeout=None)
        
        names = [
            "McPlayHD","BridgerLand","Distance"
        ]
        buttons = [
            Button(label=name, style=discord.ButtonStyle.blurple if name != "Distance" else discord.ButtonStyle.green,
                    custom_id=f"{name.replace(' ','_')}+{tag}")
            for name in names
        ]
        for button in buttons:
            self.add_item(button)

class DeleteButton(View):
    def __init__(self, category, index):
        super().__init__()
        buttons = [Button(label="Delete", style=discord.ButtonStyle.red, custom_id="Delete"),
                         Button(label="Cancel", style=discord.ButtonStyle.gray, custom_id="Cancel")]

        async def button_callback(interaction: discord.Interaction):
            if not(interaction.user.guild_permissions.administrator):
                await interaction.response.send_message("What are you trying to do? :clown:")
                return
            
            custom_id = interaction.data["custom_id"]
            if custom_id == "Delete":
                global leaderboard_dict
                leaderboard_dict = load_json(leaderboard_path)
                delete_run = leaderboard_dict[category].pop(index)
                print(delete_run)
                save_json(leaderboard_path,leaderboard_dict)
                obsolete_substitution(delete_run = delete_run)
                save_json(leaderboard_path,leaderboard_dict)
                save_json(obsolete_path,obsolete_dict)
                await interaction.response.send_message("The run would be gone(for a really long time)")
            elif custom_id == "Cancel":
                await interaction.response.send_message("Gave bro a chance, but it hestitated :clown:")
            await interaction.message.edit(view = None)
        
        for button in buttons:
            button.callback = button_callback
            self.add_item(button)
        
        def obsolete_substitution(delete_run):
            global obsolete_dict
            obsolete_dict = load_json(obsolete_path)
            global leaderboard_dict
            leaderboard_dict = load_json(leaderboard_path)
            if obsolete_dict.get(category, None) is None:
                print("no obsolete runs")
                return
            if len(obsolete_dict[category]) == 0:
                print("no obsolete runs")
                return
            for i, run in enumerate(obsolete_dict[category]):
                if run["Runner id"] == delete_run["Runner id"]:
                    if run.get("Telly?", None) is run.get("Telly?", None):
                        sub_run = obsolete_dict[category].pop(i)
                        if "Time" in sub_run:
                            focus, flipq = "Time", True
                        else:
                            focus, flipq = "Distance", False
                        
                        focus_value = sub_run[focus]
                        for i, run in enumerate(leaderboard_dict[category]):
                            if ((focus_value > run[focus]) ^ flipq) and focus_value != run[focus]:
                                leaderboard_dict[category].insert(i, sub_run)
                                return
                        leaderboard_dict[category].append(sub_run)
                        return
            print("no substitution run")

async def dm_user(bot, user_id, message):
    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
    except Exception as e:
        print(f"unable to contact the runner with id '{user_id}'")

async def get_user_name(bot, user_id, fail_msg = None , ctx = None):
    try:
        user = await bot.fetch_user(user_id)
        return user.name
    except Exception as e:
        if fail_msg is None:
            print(f"Error fetching user with ID {user_id}: {e}")
        elif not(ctx is None):
            await ctx.send(fail_msg)
        return None

async def send_submission(bot, run_id, value, tellyq, newq = True):
    try:
        pending_run = load_json(pending_path)[str(run_id)]
    except Exception as e:
        print(pending_dict)
        print(f"here {e}")
    channel = bot.get_channel(submisson_channel_id)

    if channel:
        view = VerificationView(run_id = run_id, bot = bot)
        message = await channel.send( "--------------------------\n"
                                    +f"Submission ID: {run_id}\n"
                                    +f"Submission by: <@{pending_run['Submitter id']}>\n"
                                    +f"Category: **{pending_run['Category']}**\n "
                                    +f"Runner: <@{pending_run['Runner id']}>\n"
                                    +f"Time (Or distance): {value}\n"
                                    +f"Video: {pending_run['Link']}\n"
                                    +f"Telly? (Straight speedrun only): {tellyq}\n"
                                    +f"Status: **Pending** :thinking:", view=view)
        pending_dict[run_id]["Message id"] = message.id
        if newq:
            global pending_id
            pending_id += 1
            pending_dict.update({"counter":pending_id})
        save_json(pending_path , pending_dict)

def is_link(link):
    link_regex = re.compile( r'^https?://')
    return re.match(link_regex, link) is not None

async def setup(bot):
    await bot.add_cog(lb(bot))
