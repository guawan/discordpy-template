import aiohttp
import discord
from discord import app_commands, Interaction
from bot_Tools.emojis import E


API_URL = "https://tinyurl.com/api-create.php?url={}"


# ===== 註冊子指令 =====
def register(group: app_commands.Group):
    @group.command(name="縮網址", description="將長網址縮短成短網址")
    async def shorten_url(interaction: Interaction, 網址: str):
        await interaction.response.defer()  # 先回應，避免等待太久

        short_url = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL.format(網址)) as resp:
                    if resp.status == 200:
                        short_url = await resp.text()
        except Exception as e:
            short_url = None

        if not short_url:
            await interaction.followup.send(f"{E.Error_1} 無法縮短該網址，請確認輸入是否正確。")
            return

        embed = discord.Embed(
            title=f"{E.Wrench} 短網址產生器",
            description="已成功縮短網址",
            color=discord.Color.green(),
        )
        embed.add_field(name="原始網址", value=f"└ {網址}", inline=False)
        embed.add_field(name="縮短後", value=f"└ {short_url}", inline=False)

        await interaction.followup.send(embed=embed)
