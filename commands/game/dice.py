import random
import discord
from discord import app_commands, Interaction, ui



# ====== 下拉選單 ======
class DiceSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1 顆骰子", value="1", emoji="🎲"),
            discord.SelectOption(label="2 顆骰子", value="2", emoji="🎲"),
            discord.SelectOption(label="3 顆骰子", value="3", emoji="🎲"),
        ]
        super().__init__(placeholder="請選擇要擲的骰子數量", options=options, custom_id="dice:select")

    async def callback(self, interaction: Interaction):
        count = int(self.values[0])

        # 玩家擲骰子
        player_rolls = [random.randint(1, 6) for _ in range(count)]
        player_total = sum(player_rolls)

        # 機器人擲骰子
        bot_rolls = [random.randint(1, 6) for _ in range(count)]
        bot_total = sum(bot_rolls)

        # 判斷結果
        if player_total > bot_total:
            result = f"你贏了！"
        elif player_total < bot_total:
            result = f"你輸了！"
        else:
            result = f"平手！"

        embed = discord.Embed(
            title=f"擲骰子遊戲",
            description=(
                f"└ 你擲出：`{player_rolls}` (總和 {player_total})\n"
                f"└ 機器人擲出：`{bot_rolls}` (總和 {bot_total})\n\n"
                f"結果：{result}"
            ),
            color=discord.Color.random()
        )
        await interaction.response.edit_message(embed=embed, view=None)


# ====== View 容器 ======
class DiceView(ui.View):
    def __init__(self):
        super().__init__(timeout=30)  # 30 秒內可選擇
        self.add_item(DiceSelect())


# ====== 註冊子指令 ======
def register(group: app_commands.Group):
    @group.command(name="擲骰子", description="和機器人比骰子大小")
    async def dice(interaction: Interaction):
        embed = discord.Embed(
            title=f"擲骰子遊戲",
            description="└ 請從下方選單選擇要擲的骰子數量！",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, view=DiceView())
