import random
import discord
from discord import app_commands, Interaction, ui
from bot_Tools.emojis import E


# ====== 下拉選單 ======
class RPSSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="剪刀", emoji="✌️"),
            discord.SelectOption(label="石頭", emoji="✊"),
            discord.SelectOption(label="布", emoji="✋"),
        ]
        super().__init__(placeholder="請選擇你的出拳", options=options, custom_id="rps:select")

    async def callback(self, interaction: Interaction):
        player_choice = self.values[0]
        bot_choice = random.choice(["剪刀", "石頭", "布"])

        if player_choice == bot_choice:
            result = f"{E.Loding} 平手！"
        elif (player_choice == "剪刀" and bot_choice == "布") or \
             (player_choice == "石頭" and bot_choice == "剪刀") or \
             (player_choice == "布" and bot_choice == "石頭"):
            result = f"{E.Salute} 你贏了！"
        else:
            result = f"{E.Error_1} 你輸了！"

        embed = discord.Embed(
            title=f"{E.Game_Controller} 剪刀石頭布",
            description=(
                f"└ 你出：**{player_choice}**\n"
                f"└ 機器人出：**{bot_choice}**\n\n"
                f"結果：{result}"
            ),
            color=discord.Color.random()
        )
        await interaction.response.edit_message(embed=embed, view=None)


# ====== View 容器 ======
class RPSView(ui.View):
    def __init__(self):
        super().__init__(timeout=30)  # 30 秒內可選擇
        self.add_item(RPSSelect())


# ====== 註冊子指令 ======
def register(group: app_commands.Group):
    @group.command(name="猜拳", description="和機器人玩剪刀石頭布")
    async def rps(interaction: Interaction):
        embed = discord.Embed(
            title=f"{E.Game_Controller} 剪刀石頭布",
            description="└ 請從下方選單選擇你的出拳！",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, view=RPSView())
