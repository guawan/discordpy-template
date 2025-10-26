import os
import time
import psutil
import platform
import discord
from discord import app_commands, Interaction
from bot_Tools.emojis import E

# 建立 Process 物件，指向目前 Bot 的進程
process = psutil.Process(os.getpid())

def register(tree):
    @tree.command(name="狀態", description="查詢機器人自身資源狀態")
    async def status(interaction: Interaction):
        # 更新進程資訊
        with process.oneshot():
            cpu_percent = process.cpu_percent(interval=0.5)
            mem_info = process.memory_info()
            mem_percent = process.memory_percent()
            threads = process.num_threads()
            handles = process.num_handles() if hasattr(process, "num_handles") else None
            uptime_seconds = time.time() - process.create_time()

        # 把秒數轉換為 d:HH:MM:SS
        days, remainder = divmod(int(uptime_seconds), 86400)
        time_str = time.strftime("%H:%M:%S", time.gmtime(remainder))
        uptime_str = f"{days} 天 {time_str}" if days else time_str

        # Discord / Python 版本
        python_version = platform.python_version()
        discord_version = discord.__version__

        # Bot 資訊
        guild_count = len(interaction.client.guilds)
        user_count = sum(g.member_count or 0 for g in interaction.client.guilds)

        embed = discord.Embed(
            title=f"{E.Setting} 機器人狀態",
            description="目前機器人本身的運行資訊",
            color=discord.Color.blurple(),
        )

        embed.add_field(name="Bot 名稱", value=f"└ {interaction.client.user}", inline=False)
        embed.add_field(name="CPU 使用率", value=f"└ {cpu_percent:.1f}%", inline=True)
        embed.add_field(
            name="記憶體使用",
            value=f"└ {mem_percent:.1f}% ({mem_info.rss // (1024**2)}MB)",
            inline=True,
        )
        embed.add_field(name="執行緒數量", value=f"└ {threads}", inline=True)
        if handles is not None:
            embed.add_field(name="開啟 Handles", value=f"└ {handles}", inline=True)
        embed.add_field(name="運行時間", value=f"└ {uptime_str}", inline=False)
        embed.add_field(name="Python 版本", value=f"└ {python_version}", inline=True)
        embed.add_field(name="discord.py 版本", value=f"└ {discord_version}", inline=True)
        embed.add_field(name="連線伺服器數", value=f"└ {guild_count}", inline=True)
        embed.add_field(name="已服務用戶數", value=f"└ {user_count}", inline=True)

        await interaction.response.send_message(embed=embed)
