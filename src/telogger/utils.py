from typing import Literal

ParseMode = Literal["HTML", "MarkdownV2", None]

def format_message(
    text: str,
    level: str = "INFO",
    parse_mode: ParseMode = "HTML"
) -> str:
    emoji_map = {
        "INFO": "ℹ️",
        "ERROR": "❌",
        "WARNING": "⚠️",
        "START": "🚀",
        "SUCCESS": "✅",
        "CRITICAL": "🔥"
    }
    emoji = emoji_map.get(level.upper(), "")
    
    if parse_mode == "HTML":
        return f"<b>{emoji} {level}</b>\n<code>{text}</code>"
    elif parse_mode == "MarkdownV2":
        return f"*{emoji} {level}*\n`{text}`"
    return f"{emoji} {level}: {text}"