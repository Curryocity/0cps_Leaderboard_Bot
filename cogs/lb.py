import discord
import json
import os
import re

from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput, Select
from discord import Embed


secret_path = "data/secret.json"
pending_path = "data/pending.json"
leaderboard_path = "data/leaderboard.json"
obsolete_path = "data/obsolete.json"
global_bot = None

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
submisson_channel_id = load_json(secret_path)["Submisson Channel id"]
pending_id = pending_dict.get("counter", None)

if pending_id is None:
    pending_id = 0
    pending_dict["counter"] = None
    save_json(pending_path, pending_dict)
    print("Error: 'counter' in pending.json is missing, please fix it as soon as possible.")

async def setup_hook(bot):
    print("Setup_hook...", end = ' ')
    pending_runs = load_json(pending_path)
    pending_runs.pop("counter")

    for i, pending_run in pending_runs.items():
        
        if "Distance" in pending_run["Category"]:
            value = pending_run["Distance"]
            tellyq = None
        else:
            value = pending_run["Time"]
            tellyq = pending_run["Telly?"]

        await send_submission(bot = bot, run_id = i, value = value, tellyq = tellyq, newq = False)
    print("Done")


class lb(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        global global_bot
        global_bot = self.bot

    @commands.command()
    async def lb(self,ctx):
        await ctx.send("Select a category:", view = InitialButton(tag = "lb"))

    @commands.command()
    async def submit(self,ctx):
        await ctx.send("Select a category to submit ur run:", view = InitialButton(tag = "submit"))

    @commands.command()
    @commands.has_any_role('Admin','admin','Moderator','moderator')
    async def delete(self, ctx, param = "", runner_id = None):
        if param == "":
            await ctx.send("## Need Help? \n ## Syntax: !delete <category tag> <runner_id>\n"+
                           "1. **m**:  McPlayHD,  **b**:  BridgerLand,  **d**:  Distance\n"+
                           "2. **Digit** for sub-category. 1-10 (0 represent 10) matching the order of !lb options\n"+
                           "3. **y/n** correspond to telly and tellyless (leave it blank if None)\n"+
                           "e.g.  ***!delete m2n ..***  means delete run from \"McPlayHD Short Tellyless%\"\n"+
                           "        ***!delete d4  ..***  means delete run from \"Distance Hold Diag Fruit\"")
        else:
            state, category, tellyq, full_name = category_interpreter(param, True)
                
            if state == 1:
                await ctx.send("Invalid category tag, !delete to check out the guide.")
                return
            if state == 2:
                await ctx.send("Invalid telly tag, !delete to check out the guide.")
                return
            if runner_id is None:
                await ctx.send("Runner id?")
                return

            runner_name = await get_user_name(self.bot, runner_id, f"I don't think there is runner with id  '{runner_id}'", ctx)
            if runner_name is None:
                return
            
            templb = load_json(leaderboard_path).get(category, None)
            if templb is None:
                await ctx.send(f"{runner_name} does not have a run in {full_name}")
                return

            for i, run in enumerate(templb):
                if run["Runner id"] == int(runner_id):
                    if tellyq is run.get("Telly?", None):
                        content = f"Are you sure to delete {runner_name}'s run in {full_name} ?"
                        await ctx.send(content, view = DeleteButton(category = category, index = i))
                        return

            await ctx.send(f"{runner_name} does not have a run in {full_name}")

    @commands.command()
    @commands.has_any_role('Admin','admin','Moderator','moderator')
    async def tie(self, ctx, param = "", rank = None, order = None):
        if param == "":
            await ctx.send("## Welcome to tie resolver! \n ## Syntax: !tie <category tag> <rank> <order>\n"+
                           "1. **m**:  McPlayHD,  **b**:  BridgerLand,  **d**:  Distance\n"+
                           "2. **Digit** for sub-category. 1-10 (0 represent 10) matching the order of !lb options\n"+
                           "3. Please put the rank as the number it appear on the lb, I am lazy to code more foolproof(it's mods' tool)\n"+
                           "4. For n ties, order is an 1-n number sequence that determine the relative order according to current order\n"+
                           "e.g.  ***!tie m2 2 321***  means fixing \"McPlayHD Short\" 2nd place ties(3 ties in total) by ordering them in reverse\n")
        else:
            state, category, tellyq, full_name = category_interpreter(param, False)
            ties = []
            
            if state == 1:
                await ctx.send("Invalid category tag, !tie to check out the guide.")
                return
            
            templb = load_json(leaderboard_path).get(category, None)
            if templb is None:
                await ctx.send(f"There is no run in \"{category}\"")
                return
            
            if rank is None:
                await ctx.send("rank?")
                return
            try:
                rank = int(rank)
            except ValueError:
                await ctx.send("Invalid rank")
                return
            
            if (rank < 1) or (rank > len(templb)):
                await ctx.send("rank out of bound")
                return
            if order is None:
                await ctx.send("order?")
                return

            if "Distance" in category:
                focus = "Distance"
            else:
                focus = "Time"

            value = templb[rank-1][focus]
            ties.append(templb[rank-1])
            ties_amount = 1
            
            for i in range(0,len(templb)-rank):
                if templb[rank+i][focus] != value:
                    break
                ties.append(templb[rank+i])
                ties_amount += 1
            
            if ties_amount == 1:
                await ctx.send(f"There is no tie at rank: {rank}")
                return
            
            if len(order) != ties_amount:
                await ctx.send(f"order sequence length should be equal to the amount of ties: {ties_amount}")
                return
            
            ordered_ties = [None] * len(ties)

            for i,t in enumerate(order):
                try:
                    placement = int(t)-1
                    if placement < 0:
                        raise ValueError
                    
                    if ordered_ties[placement] is None:
                        ordered_ties[placement] = ties[i]
                    else:
                        raise ValueError
                except:
                    await ctx.send(f"Error while iterating through ur 'order' sequence")
                    return

            for i,t in enumerate(ordered_ties):
                templb[rank-1+i] = t
            global leaderboard_dict
            leaderboard_dict = load_json(leaderboard_path)
            leaderboard_dict[category] = templb
            save_json(leaderboard_path, leaderboard_dict)

            await ctx.send("Reordered the ties successfully")
                
class InitialButton(View):
    def __init__(self, tag : str, selected = 0):
        super().__init__(timeout=None)

        self.selected = selected
        self.tag = tag
        self.names = ["McPlayHD", "BridgerLand", "Distance"]

        self.update_buttons()
    
    def update_buttons(self):
        self.clear_items()

        for i, name in enumerate(self.names):
            button = Button(
                label=name, 
                style=discord.ButtonStyle.grey if (i + 1) != self.selected else discord.ButtonStyle.blurple,
                custom_id=f"{name.replace(' ', '_')}+{self.tag}"
            )
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction: discord.Interaction):

        custom_id = interaction.data["custom_id"]
        category, tag = custom_id.split('+')

        if tag == "lb":
            content = "Select a category:"
        elif tag == "submit":
            content = "Select a category to submit ur run:"

        if category == "McPlayHD":
            self.selected = 1
            placeholder = "Select a sub-category for McPlayHD:"
        elif category == "BridgerLand":
            self.selected = 2
            placeholder = "Select a sub-category for BridgerLand:"
        elif category == "Distance":
            self.selected = 3
            placeholder = "Select a sub-category for Distance:"

        self.update_buttons()
        self.add_item(CategorySelect(category = category, tag = tag, placeholder = placeholder))

        await interaction.response.edit_message(content = content, view = self, embed = None)

class CategorySelect(Select):
    def __init__(self, category, tag, placeholder):
        options_dict = {
            "McPlayHD" : ["Extra Short", "Short", "Normal", "Long", "Inclined Short", "Inclined Normal", "Onestack"],
            "BridgerLand" : ["Short", "Regular", "Inclined"],
            "Distance" : ["Cha Cha", "HGB", "Dao Telly", "Hold Diag Fruit", "Lightning", "Kemytz Bridge", "Gain Cha Cha", "Hold Space Haka", "Hold Durx"]
        }
        options = [discord.SelectOption(label = option) for option in options_dict[category]]
        super().__init__(placeholder = placeholder, options = options) # value is the label name by default
        self.category = category
        self.tag = tag

    async def callback(self, interaction: discord.Interaction):
        if self.tag == "submit":
                    modal = SubmitGUI(category= f"{self.category} {self.values[0]}", submitter_id= interaction.user.id)
                    await interaction.response.send_modal(modal)
        elif self.tag == "lb":
            title, content = generatelb(category = f"{self.category} {self.values[0]}")
            if title is None:
                await interaction.response.edit_message(content = content, embed = None)
            else:
                embed = Embed(title = title, description = content, color = 0xa800e6)
                await interaction.response.edit_message(content = "",embed = embed)

def generatelb(category):
    content = ""
    tempLB = load_json(leaderboard_path).get(category, [])
    if not tempLB:
        title = None
        content = f"There's no runs in **{category}** :sob:"
    else:
        tellyless_exist = False
        rank = 1
        prevalue = 0
        title = f"Leaderboard - **{category}**"
        content = ""
        if "Distance" in category:

            for i, run in enumerate(tempLB):

                if run['Distance'] != prevalue:
                    rank = i + 1

                content += f"- **{rank}.**  <@{run['Runner id']}>  **[{run['Distance']}b](<{run['Link']}>)**\n"
                prevalue = run['Distance']
        else:
            for i, run in enumerate(tempLB):

                if run['Time'] != prevalue:
                    rank = i + 1

                if run["Telly?"] is False:
                    content += f"- **{rank}.**  :sloth: <@{run['Runner id']}>   **[{run['Time']}s](<{run['Link']}>)**\n"
                    tellyless_exist = True
                else:
                    content += f"- **{rank}.**  <@{run['Runner id']}>   **[{run['Time']}s](<{run['Link']}>)**\n"

                prevalue = run['Time']
        content +=  ("\u00a0" * 111) + "\n" 
        if tellyless_exist: content += ("(:sloth: --> the run is performed ***tellyless***)")

    return title, content

class SubmitGUI(Modal, title = "Submit your run"):
    def __init__(self, category, submitter_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global global_bot
        self.bot = global_bot
        self.category = category
        self.submitter_id = submitter_id
        self.submitter_name = None
        self.runner_id = self.submitter_id
        self.runner_name = None

        if "Distance" in self.category:
            self.add_item(TextInput(label="Distance", placeholder="Unit: block(s)"))
        else:
            self.add_item(TextInput(label="Time", placeholder="Unit: second(s)"))
            if not("Inclined" in self.category) and not("Onestack" in self.category):
                self.add_item(TextInput(label="Sprint restriction?", placeholder="'0' if telly%, '1' if tellyless%"))

        self.add_item(TextInput(label= "Video Link", placeholder="Paste a permanent & direct link"))
        self.add_item(TextInput(label = "Runner id", placeholder="Leave it blank if you're the runner", required= False))

    async def on_submit(self, interaction: discord.Interaction):
        global pending_id
        self.submitter_name = await get_user_name(self.bot, self.submitter_id)
        self.runner_name = self.submitter_name
        value = self.children[0].value

        tellyq = None
        if not(("Distance" in self.category) or ("Inclined" in self.category) or ("Onestack" in self.category)):
            if self.children[1].value == "0":
                tellyq = True
            elif self.children[1].value == "1":
                tellyq = False
            else:
                await interaction.response.send_message(f"You should only put 0 or 1 in the 'Rescriction mode', read the rule for further info.")
                return
            
        link = self.children[-2].value
        if not(is_link(link)):
            await interaction.response.send_message(f"Invalid link, you failed the world's most lenient link test :thumbsup:")
            return
        
        if self.children[-1].value != "":
            self.runner_id = self.children[-1].value
            self.runner_name = await get_user_name(self.bot, self.runner_id)
            if self.runner_name is None:
                await interaction.response.send_message(f"I cun't fetch runner id, plz chuck if the id were valid.")
                return
        try: # when you're too bored:
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
                    await interaction.response.send_message(f"Minecraft runs on tick(0.05s) dummy. You -> {value}s :skull:")
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
        self.required_roles = ['Admin', 'admin', 'Moderator', 'moderator']
    


    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not(any(role.name in self.required_roles for role in interaction.user.roles)):
            await interaction.response.send_message("What are you trying to do? :clown:", ephemeral=True)
            return
        
        await interaction.response.defer()
        submission = pending_dict.pop(self.run_id, None)
        if submission:
            self.insertLB(submission["Category"], submission)
            save_json(pending_path , pending_dict)
            save_json(leaderboard_path, leaderboard_dict)
            save_json(obsolete_path, obsolete_dict)
            
            await dm_user(self.bot, submission["Runner id"], f"Your submission for the category **{submission['Category']}** has been verified and added to the leaderboard.")
            channel = self.bot.get_channel(submisson_channel_id)
            
            if channel:
                message = await channel.fetch_message(submission["Message id"])
                embed = message.embeds[0]  
                new_description = embed.description.replace("**Pending** :thinking:", "**Verified** :white_check_mark:")
                embed.description = new_description
                await message.edit(embed=embed, view=None)
        else:
            await interaction.response.send_message('The submission could not be found.', ephemeral=True)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not(any(role.name in self.required_roles for role in interaction.user.roles)):
            await interaction.response.send_message("What are you trying to do? :clown:", ephemeral=True)
            return
        
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
        await interaction.response.defer()
        try:
            if self.submission:
                await dm_user(self.bot, self.submission["Runner id"],f"Fortunately, your submission to the {self.submission['Category']} leaderboards has been rejected for the reason: ***{reason}***.\n~~*(Feel free to cry if you believe this is wrong or unjustified)*~~")
                channel = self.bot.get_channel(submisson_channel_id)
                if channel:
                    message = await channel.fetch_message(self.submission["Message id"])
                    embed = message.embeds[0]  
                    new_description = embed.description.replace("**Pending** :thinking:", f"**Rejected** :x:\n**Reason: {reason}**")
                    embed.description = new_description
                    await message.edit(embed=embed, view=None)
                save_json(pending_path, pending_dict)
            else:
                print(f"submission {self.run_id} not found")
            
        except Exception as e:
            pending_dict.append(self.submission)
            await interaction.response.send_message(f"Error msg: {e}\nPlease try again, it should be working fine. Hope it is Discord's issue", ephemeral=True)

class DeleteButton(View):
    def __init__(self, category, index):
        super().__init__()
        buttons = [Button(label="Delete", style=discord.ButtonStyle.red, custom_id="Delete"),
                    Button(label="Cancel", style=discord.ButtonStyle.gray, custom_id="Cancel")]

        async def button_callback(interaction: discord.Interaction):
            if not(any(role.name in self.required_roles for role in interaction.user.roles)):
                await interaction.response.send_message("What are you trying to do? :clown:", ephemeral=True)
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
            print("Random log: No runs for substitution")

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
        content = (
                 f"Submission by: <@{pending_run['Submitter id']}>\n"
                +f"Category: **{pending_run['Category']}**\n"
                +f"Runner: <@{pending_run['Runner id']}>\n"
                +f"Time (Or distance): **{value}**\n"
                +f"Video: **{pending_run['Link']}**\n"
                +f"Telly? (Straight speedrun only): **{tellyq}**\n"
                +f"Status: **Pending** :thinking:")
        embed = Embed(title = f"Submission ID: {run_id}", description = content, color = 0xa800e6 )
        message = await channel.send(content = "", embed = embed, view=view)
        pending_dict[run_id]["Message id"] = message.id
        if newq:
            global pending_id
            pending_id += 1
            pending_dict.update({"counter":pending_id})
        save_json(pending_path , pending_dict)

def category_interpreter(param: str, tellymatter: bool):
    param = param.lower()
    tellyq = None
    state = 1
    category, full_name = "", ""

    if tellymatter:
        if param.endswith("y"):
            tellyq = True
            param = param.removesuffix("y")
        elif param.endswith("n"):
            tellyq = False
            param = param.removesuffix("n")

        tellyreq = ["m1","m2","m3","m4","b1","b2"]

    category_map = {"m1":"McPlayHD Extra Short", "m2":"McPlayHD Short", "m3":"McPlayHD Normal", "m4":"McPlayHD Long", "m5":"McPlayHD Inclined Short", "m6":"McPlayHD Inclined Normal", "m7":"McPlayHD Onestack",
                    "b1":"BridgerLand Short", "b2":"BridgerLand Regular", "b3":"BridgerLand Inclined",
                    "d1":"Distance Cha Cha", "d2":"Distance HGB","d3":"Distance Dao Telly","d4":"Distance Hold Diag Fruit","d5":"Distance Lightning","d6":"Distance Kemytz Bridge","d7":"Distance Gain Cha Cha","d8":"Distance Hold Space Haka","d9":"Distance Hold Durx"}
    if param in category_map:
        
        category = category_map[param]
        if tellymatter:
            full_name = category
            state = 2
            if (param in tellyreq) ^ (tellyq is None):
                if tellyq is True:
                    full_name += " Telly%"
                elif tellyq is False:
                    full_name += " Tellyless%"
                state = 0
        else:
            state = 0
    return state, category, tellyq, full_name #state == 0 means success

def is_link(link):
    link_regex = re.compile( r'^https?://')
    return re.match(link_regex, link) is not None

async def setup(bot):
    await bot.add_cog(lb(bot))
