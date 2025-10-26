# bot.py
import os
import asyncio
import logging
import warnings
import discord
import itertools
from discord.ext import commands, tasks
from bot_Tools.main_groups import setup_app_command_groups
from bot_Tools.emojis import bind_emojis_client
from dotenv import load_dotenv

# 忽略 discord.py 內部的警告訊息 (PyNaCl, intent 之類)
warnings.filterwarnings("ignore", category=UserWarning)

# 載入 .env 檔案
load_dotenv()

# 簡單輸出格式
logging.basicConfig(level=logging.INFO, format="%(message)s")

# 把 discord logger 壓到 WARNING
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)
logging.getLogger("discord.ext").setLevel(logging.WARNING)

# 讀取 Token
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN 沒有設定，請在 .env 中新增 BOT_TOKEN=你的Token")

# 部分意圖
# intents = discord.Intents.none()
# intents.guilds = True
# intents.message_content = True

# 給予全部意圖
intents = discord.Intents.all()

# prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 狀態輪替 =====
# itertools.cycle：建立一個無限循環的清單
activities = itertools.cycle([
    discord.Game("123"),
    discord.Game("456"),
    discord.Game("789"),

])

@tasks.loop(seconds=30)  # 每 30 秒切換一次
async def status_loop():
    next_activity = next(activities)
    await bot.change_presence(
        status=discord.Status.online,  # 可以改成 idle 或 dnd
        activity=next_activity
    )

@status_loop.before_loop
async def before_status_loop():
    await bot.wait_until_ready()


# 註冊事件 
@bot.event 
async def on_ready():
    # 建立/載入所有主群組指令（依照 MAIN_COMMANDS 掃描子指令）
    setup_app_command_groups(bot.tree)

    # 綁定自訂表情（讓 E.OK / E.ERROR 等能正常使用）
    bind_emojis_client(bot)

    # 將 Slash 指令同步到所有 Guild
    synced = await bot.tree.sync()
    logging.info("🎵 Slash 指令已同步到所有 Guild")
    logging.info("🎵 已登入 %s", bot.user)

    # 啟動狀態輪替
    if not status_loop.is_running():
        status_loop.start()


# 啟動後台任務
if __name__ == "__main__":
    bot.run(TOKEN)
