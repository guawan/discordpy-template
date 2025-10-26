# emojis.py
"""
集中管理機器人的自訂表情符號。
只要在 EMOJI_CONFIG 裡新增 ID，就能全域 import E 使用。

使用方式：
    from emojis import E
    await ctx.send(f"{E.SUCCESS1} 完成 {E.ERROR1}")

啟動時在 bot.py 的 on_ready 呼叫 bind_emojis_client(bot)。
"""

from typing import Optional, Dict, Tuple, Protocol
import discord

# ===== 1) 在這裡新增自訂表情 =====
# 格式: "代號": (表情 ID, 是否動畫)
EMOJI_CONFIG: Dict[str, Tuple[int, bool]] = {
    "Error_1": (1412045710827978772, True),
    "Success_1": (1412045700052811817, True),
    "Error_2": (1412037090128039967, True),
    "Success_2": (1412034390082715740, True),
    "Arrow": (1412042942448930856, True),
    "Loding": (1412040159892996168, True),  
    "Salute": (1412037176828366908, True),
    "Wrning": (1412037149716385924, True),   
    "Notify_1": (1412037119253286952, True),
    "Notify_2": (1412037109463908494, True),
    "Game_Controller": (1415825896857796608, False),
    "Setting": (1415830712476631192, False),
    "Wrench": (1415836395557097544, False),
}


# ===== 2) 型別提示 (給編輯器用，方便補全) =====
class EmojiBagProto(Protocol):
    Error_1: str
    Success_1: str
    Error_2: str
    Success_2: str
    Arrow: str
    Loding: str
    Salute: str
    Wrning: str
    Notify_1: str
    Notify_2: str
    Game_Controller: str
    Setting: str
    Wrench: str


# ===== 3) 動態 EmojiBag =====
class EmojiBag:
    """一個動態物件，屬性對應 EMOJI_CONFIG 的 key。"""
    def __init__(self, mapping: Dict[str, str]):
        for k, v in mapping.items():
            setattr(self, k, v)

    def __getattr__(self, item: str) -> str:
        raise AttributeError(f"Emoji '{item}' 尚未在 EMOJI_CONFIG 中定義")

    def __dir__(self):
        # 讓 dir(E) 時能看到所有 key
        return list(super().__dir__()) + list(EMOJI_CONFIG.keys())


# ===== 4) Emoji 管理器 =====
class _EmojiManager:
    def __init__(self) -> None:
        self._client: Optional[discord.Client] = None
        self._bag: Optional[EmojiBag] = None

    def _resolve(self, key: str, eid: int, animated: bool) -> str:
        """將 ID + animated 轉為 <a:name:id> 或 <:name:id>。"""
        if not self._client:
            return f"<{'a' if animated else ''}:{key}:{eid}>"
        emoji = self._client.get_emoji(eid)
        if emoji:
            return str(emoji)
        return str(discord.PartialEmoji(name=key.lower(), id=eid, animated=animated))

    def _build_bag(self) -> EmojiBag:
        resolved = {k: self._resolve(k, v[0], v[1]) for k, v in EMOJI_CONFIG.items()}
        return EmojiBag(resolved)

    def bind_client(self, client: discord.Client) -> None:
        self._client = client
        self._bag = self._build_bag()

    @property
    def bag(self) -> EmojiBag:
        if self._bag is None:
            self._bag = self._build_bag()
        return self._bag


# ===== 5) 對外接口 =====
_manager = _EmojiManager()
E: EmojiBagProto = _manager.bag  # 型別提示給 IDE

def bind_emojis_client(client: discord.Client) -> None:
    """在 bot.py on_ready 呼叫，解析 ID 成真正的表情字串。"""
    _manager.bind_client(client)
    globals()["E"] = _manager.bag
