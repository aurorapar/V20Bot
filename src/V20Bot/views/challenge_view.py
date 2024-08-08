import discord

from discord.ui import Button, Select, TextInput

from ..character.attribute import PhysicalAttribute
from ..character.discipline import PhysicalDiscipline
from ..settings import willpower_icon
from ..settings import DICE_POOL_MODIFIER_RANGE, PHYSICAL_ATTRIBUTE_BLOOD_SPEND_CAP
from ..user_data_objects import UserData


class ChallengeView(discord.ui.View):

    def __init__(self, player: discord.Member, attribute: str, ability: str, discipline: str, timeout=30, *args, **kwargs):
        super(ChallengeView, self).__init__(timeout=timeout, *args, **kwargs)

        self.edit_original_response: None
        self.attribute = attribute
        self.ability = ability
        self.discipline = discipline
        self.user = UserData(player.id)
        self.willpower_spent = False
        self.physical_spends = 0
        self.discipline_activated = False
        self.adjustment = 0
        self.blood_spent = self.physical_spends + int(self.discipline_activated)
        self.specialized = False

        self.difficulty = 0
        self.dice_pool =\
            self.user.UserData[attribute] +\
            (self.user.UserData[ability] if ability in self.user.UserData.keys() else 0) + \
            (self.user.UserData[discipline] if discipline in self.user.UserData.keys() else 0)
        self.auto_successes = 0
        self.base_message = f"Difficulty: {self.difficulty}\tDice Pool: {self.dice_pool}\n" + \
                            f"Willpower Spent: {self.willpower_spent}\tSpecialized: {'No' if not self.specialized else 'Yes'}\n" + \
                            f"\tAutoSuccesses: {self.auto_successes}\tBlood Spent: {self.blood_spent}\n\n" + \
                            f"Select the difficulty, then click the buttons below to spend Willpower and Blood, then the checkmark once you're finished.\n\n"

        self.row = 0

        modifiers = [discord.SelectOption(label=str(x)) for x in range(1, 11)]
        self.difficulty_select = Select(row=self.row, custom_id="difficulty-select", options=modifiers,
                                               placeholder="Difficulty")
        self.difficulty_select.callback = self.set_difficulty
        self.add_item(self.difficulty_select)

        self.row += 1

        modifiers = [discord.SelectOption(label=str(x)) for x in range(-DICE_POOL_MODIFIER_RANGE, DICE_POOL_MODIFIER_RANGE+1)]
        self.additional_modifier_menu = Select(row=self.row, custom_id="dicepool-modifier", options=modifiers,
                                               placeholder="Dice Pool Mod")
        self.additional_modifier_menu.callback = self.adjust_dice_pool
        self.add_item(self.additional_modifier_menu)

        self.row += 1
        self.willpower_button = Button(label="Spend Willpower", row=self.row, custom_id="willpower-button",
                                       style=discord.ButtonStyle.primary, emoji=willpower_icon)
        self.willpower_button.callback = self.willpower_button_callback
        self.add_item(self.willpower_button)

        if discipline in PhysicalDiscipline and discipline in self.user.UserData.keys() and self.user.UserData[discipline] > 0:
            self.discipline_button = Button(label=f"Spend Blood for {discipline}", row=self.row, custom_id="discipline-button",
                                                    style=discord.ButtonStyle.primary, emoji="🩸")
            self.discipline_button.callback = self.activate_discipline
            self.add_item(self.discipline_button)

        self.specialization_entry = Button(label="Specialized", row=self.row, custom_id="specialization-button",
                                              style=discord.ButtonStyle.primary, emoji="👩‍⚕️")
        self.specialization_entry.callback = self.specialization_handler
        self.add_item(self.specialization_entry)

        if attribute in PhysicalAttribute and attribute in self.user.UserData.keys() and self.user.UserData[attribute] > 0:
            self.row += 1
            self.blood_buttons = []
            for count in range(1, PHYSICAL_ATTRIBUTE_BLOOD_SPEND_CAP+1):
                self.blood_buttons.append(Button(label=f"Spend {count} Blood for {attribute}", row=self.row,
                                              custom_id=f"blood-button-{count}", style=discord.ButtonStyle.primary,
                                              emoji="🩸"))
                self.blood_buttons[-1].callback = self.spend_blood
                self.add_item(self.blood_buttons[-1])

        self.row += 1
        self.activation_button = Button(label=f"Click when you're finished", row=self.row, custom_id = "check-button",
                                        style=discord.ButtonStyle.primary, emoji="✔️")
        self.activation_button.callback = self.finished_selecting
        self.add_item(self.activation_button)

        self.update_message_values()

        self.components_list = [self.difficulty_select, self.additional_modifier_menu, self.willpower_button,
                                self.discipline_button, self.blood_buttons, self.activation_button]

    def update_message_values(self):
        self.blood_spent = self.physical_spends + int(self.discipline_activated)

        self.dice_pool = (
            (self.user.UserData[self.attribute] + self.physical_spends) +\
            (self.user.UserData[self.ability] if self.ability in self.user.UserData.keys() else 0) + \
            (self.user.UserData[self.discipline] if self.discipline in self.user.UserData.keys() else 0)
        )

        self.auto_successes = (
            int(self.willpower_spent) +\
            (self.user.UserData[self.discipline] if self.discipline in self.user.UserData.keys() and self.discipline_activated else 0)
        )

    async def update_message(self, addition="", *args, **kwargs):
        self.blood_spent = self.physical_spends + int(self.discipline_activated)

        self.dice_pool = (
            (self.user.UserData[self.attribute] + self.physical_spends) +
            (self.user.UserData[self.ability] if self.ability in self.user.UserData.keys() else 0) +
            (self.user.UserData[self.discipline] if self.discipline in self.user.UserData.keys() else 0) +
            self.adjustment
        )

        self.auto_successes = (
            int(self.willpower_spent) +\
            (self.user.UserData[self.discipline] if self.discipline in self.user.UserData.keys() and self.discipline_activated else 0)
        )

        self.base_message = f"Difficulty: {self.difficulty}\tDice Pool: {self.dice_pool}\n" + \
                            f"Willpower Spent: {self.willpower_spent}\tSpecialized: {'No' if not self.specialized else self.specialized}\n" + \
                            f"\tAutoSuccesses: {self.auto_successes}\tBlood Spent: {self.blood_spent}\n\n" + \
                            (addition if addition else f"Select the difficulty, then click the buttons below to spend Willpower and Blood, then the checkmark once you're finished.\n\n")
        await self.edit_original_response(content=self.base_message, *args, **kwargs)

    async def willpower_button_callback(self, interaction):
        self.willpower_spent = not self.willpower_spent
        self.willpower_button.label = "Stop Spending Willpower" if self.discipline_activated else "Spend Willpower"
        await interaction.response.send_message(f"You are {'not ' if not self.willpower_spent else ''}spending Willpower", ephemeral=True)
        await self.update_message()

    async def spend_blood(self, interaction):
        custom_id = interaction.data['custom_id']
        button = [b for b in self.blood_buttons if b.custom_id == custom_id][0]
        count = int(custom_id.split('-')[-1])
        if count == self.physical_spends:
            button.label = f"Spend {count} Blood for {self.attribute}"
            self.physical_spends -= count
            await interaction.response.send_message(f"You are no longer spending blood on {self.attribute} ({self.attribute} at {self.user.UserData[self.attribute]})")
        else:
            button.label = f"Stop Spending {count} Blood for {self.attribute}"
            await interaction.response.send_message(f"You are spending {count} blood to raise your {self.attribute} to {self.user.UserData[self.attribute] + count}")
            self.physical_spends = count
        await self.update_message()

    async def activate_discipline(self, interaction):
        self.discipline_activated = not self.discipline_activated
        self.discipline_button.label = "Stop Spending Blood on Potence" if self.discipline_activated else "Spend Blood on Potence"
        self.auto_successes += self.user.UserData[self.discipline] * 1 if self.discipline_activated else self.user.UserData[self.discipline] * -1
        await interaction.response.send_message(f"You are {'not ' if not self.discipline_activated else ''}spending Blood on {self.discipline}", ephemeral=True)
        await self.update_message()

    async def specialization_handler(self, interaction):
        self.specialized = not self.specialized
        await interaction.response.send_message(f"You are {'not ' if not self.specialized else ''}Specialized", ephemeral=True)
        await self.update_message()

    async def adjust_dice_pool(self, interaction):
        self.adjustment = int(list(interaction.data.values())[0][0])
        self.additional_modifier_menu.placeholder = f"Dice Pool Adjustment of {self.adjustment}"
        await interaction.response.send_message(f"New Dice Pool adjustment of {self.adjustment}")
        await self.update_message()

    async def set_difficulty(self, interaction):
        self.difficulty = int(list(interaction.data.values())[0][0])
        self.difficulty_select.placeholder = f"Difficulty {self.difficulty}"
        await interaction.response.send_message(f"New Difficulty of {self.difficulty}")
        await self.update_message()

    async def finished_selecting(self, interaction):
        if self.difficulty < 1:
            await interaction.response.send_message(content=f"You can't finish without selecting the difficulty.", ephemeral=True)
            return
        if self.dice_pool < 1:
            await interaction.response.send_message(content=f"You can't engage in the challenge without a dice pool.", ephemeral=True)
            return
        await self.update_message(addition=f"You have locked in your choices!", view=None)
