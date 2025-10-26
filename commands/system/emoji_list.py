# commands/system/emoji_list.py
import discord
from discord import app_commands, Interaction
from bot_Tools.emojis import E

def register(tree):
    @tree.command(name="表情清單", description="查看機器人所有可用表情")
    async def show_emojis(interaction: Interaction):
        embed = discord.Embed(
            title=f"{E.Setting} 機器人表情清單",
            description=f"{E.Arrow}以下是機器人當前可用的表情",
            color=discord.Color.green(),
        )

        # 只列出 EmojiBag 實例的屬性
        lines = []
        for key, emoji in E.__dict__.items():
            if key.startswith("_"):  # 跳過內建屬性
                continue
            lines.append(f"{emoji} **{key}**")

        embed.add_field(
            name="表情符號清單：",
            value="\n".join(lines) or "（尚未設定表情）",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
