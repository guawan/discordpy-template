# commands/main_groups.py
"""
集中定義主指令群組，並自動載入子指令檔案。
- 只需在 MAIN_COMMANDS 加一行：資料夾 -> (主指令名稱, 描述)
- 群組名稱可以中文，資料夾建議英文
- 若該群組找不到任何子指令，預設「不掛群組」（避免後台報錯）
  - 可切換 AUTO_ATTACH_PLACEHOLDER=True 來自動加上一個「說明」子指令
"""

import importlib
import pkgutil
from typing import Dict, Tuple
from discord import app_commands, Interaction

# ================== 使用者需編輯的區域 ==================

# key: 子指令資料夾名稱（英文）；value: (主指令名稱，可用中文, 指令描述)
MAIN_COMMANDS: Dict[str, Tuple[str, str]] = {
    # 範例：
    # "order": ("order", "訂單相關操作"),
    # "member": ("member", "成員相關功能"),
    # 中文主指令示例（資料夾 fun 對應 /休閒）：
    "system": ("系統", "系統相關功能"),
    "game": ("遊戲", "遊戲相關功能"),
    "tools": ("工具", "實用工具"),
}

# 找不到任何子指令時的行為：
SKIP_EMPTY_GROUPS = True          # True: 直接略過，不掛這個群組（建議）
AUTO_ATTACH_PLACEHOLDER = False   # False: 不自動附加佔位；True: 自動附加「說明」子指令

PLACEHOLDER_CMD_NAME = "說明"      # 佔位子指令名稱（只在 AUTO_ATTACH_PLACEHOLDER=True 時使用）

# =======================================================


def _load_subcommands_for(group: app_commands.Group, package_name: str) -> int:
    """
    掃描指定 package（如 commands.order），呼叫各子檔案的 register(group)。
    回傳本次實際掛上的子指令數量。
    """
    try:
        pkg = importlib.import_module(package_name)
    except ModuleNotFoundError:
        return 0  # 沒有這個資料夾

    before = len(group.commands)

    for modinfo in pkgutil.iter_modules(pkg.__path__):
        if modinfo.name.startswith("_"):  # 跳過 __init__ 等隱藏檔
            continue

        module = importlib.import_module(f"{package_name}.{modinfo.name}")
        # 規範：子檔需提供 register(group)
        if hasattr(module, "register") and callable(module.register):
            module.register(group)

    after = len(group.commands)
    return max(0, after - before)


def _attach_placeholder_help(group: app_commands.Group) -> None:
    """
    附加一個佔位的 /<group> <說明> 子指令，避免空群組造成報錯。
    僅在 AUTO_ATTACH_PLACEHOLDER=True 時調用。
    """
    @group.command(name=PLACEHOLDER_CMD_NAME, description=f"{group.name} 群組的說明")
    async def _placeholder(interaction: Interaction):
        await interaction.response.send_message(
            f"「/{group.name}」目前尚未配置任何子指令。請稍後再試或聯繫管理員。",
            ephemeral=True
        )


def setup_app_command_groups(tree) -> None:
    """
    由 bot.py -> on_ready() 呼叫。
    1) 清除舊指令（避免重複）
    2) 依 MAIN_COMMANDS 建群組
    3) 掃描對應資料夾，註冊子指令
    4) 若找不到子指令 → 依策略略過或附加佔位
    """
    # Step 1. 清掉舊的
    for cmd in list(tree.get_commands()):
        tree.remove_command(cmd.name, type=cmd.type)

    # Step 2~4. 建立群組並載入子指令
    for folder, (cmd_name, desc) in MAIN_COMMANDS.items():
        group = app_commands.Group(name=cmd_name, description=desc)

        loaded_count = _load_subcommands_for(group, f"commands.{folder}")

        if loaded_count == 0:
            if SKIP_EMPTY_GROUPS and not AUTO_ATTACH_PLACEHOLDER:
                # 完全略過，避免出現「只有主指令、沒有子指令」導致報錯
                continue
            if AUTO_ATTACH_PLACEHOLDER:
                _attach_placeholder_help(group)  # 附加一個「說明」子指令

        # 走到這裡表示：有子指令，或已附加佔位，才會真正掛到樹上
        tree.add_command(group)
