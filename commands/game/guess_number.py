# commands/game/guess_number.py
import random
import discord
from discord import app_commands, Interaction, ui
from bot_Tools.emojis import E

# ===== 猜數字遊戲 View =====
class GuessNumberView(ui.View):
    def __init__(self, answer: int, min_val: int, max_val: int):
        super().__init__(timeout=None)
        self.answer = answer
        self.min_val = min_val
        self.max_val = max_val

    @ui.button(label="猜數字", style=discord.ButtonStyle.primary, custom_id="guess:start")
    async def start_guess(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_modal(GuessNumberModal(self))


# ===== 猜數字表單 =====
class GuessNumberModal(ui.Modal, title="🎲 請輸入你的猜測"):
    def __init__(self, view: GuessNumberView):
        super().__init__()
        self.view = view

        self.number_input = ui.TextInput(
            label=f"數字範圍 {self.view.min_val} ~ {self.view.max_val}",
            placeholder="輸入數字",
            required=True,
        )
        self.add_item(self.number_input)

    async def on_submit(self, interaction: Interaction):
        try:
            guess = int(self.number_input.value)
        except ValueError:
            await interaction.response.send_message(f"{E.Wrning} 請輸入有效數字！", ephemeral=True)
            return

        if guess <= self.view.min_val or guess >= self.view.max_val:
            await interaction.response.send_message(
                f"{E.Wrning} 目前可猜範圍：{self.view.min_val} ~ {self.view.max_val}", ephemeral=True
            )
            return

        if guess == self.view.answer:
            embed = make_game_embed(self.view.min_val, self.view.max_val, self.view.answer, "🎉 猜對了！")
            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.send_message(f"{E.Salute} 恭喜！答案是 **{self.view.answer}**")
            return

        # 更新範圍
        if guess < self.view.answer:
            self.view.min_val = guess
            result = f"{E.Wrning} {guess} 太小了！"
        else:
            self.view.max_val = guess
            result = f"{E.Wrning} {guess} 太大了！"

        # 更新 Embed
        embed = make_game_embed(self.view.min_val, self.view.max_val, None, result)
        await interaction.message.edit(embed=embed, view=self.view)
        await interaction.response.send_message(result, ephemeral=True)


# ===== Embed 工具函式 =====
def make_game_embed(min_val: int, max_val: int, answer: int | None = None, hint: str | None = None) -> discord.Embed:
    embed = discord.Embed(
        title=f"{E.Game_Controller} 猜數字遊戲",
        description="└ 我已經想好了一個數字，來挑戰看看吧！",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="目前範圍", value=f"└ {min_val} ~ {max_val}", inline=False)
    return embed


# ===== 註冊指令 =====
def register(group: app_commands.Group):
    @group.command(name="猜數字", description="開始一場 1~100 的猜數字遊戲")
    async def guess_number(interaction: Interaction):
        min_val, max_val = 1, 100
        answer = random.randint(min_val, max_val)
        view = GuessNumberView(answer, min_val, max_val)
        embed = make_game_embed(min_val, max_val)
        await interaction.response.send_message(embed=embed, view=view)
