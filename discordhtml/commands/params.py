from typing import Any
import discord

MISSING = discord.utils.MISSING


class Parameter:
    def __init__(self, name: str, default: Any = MISSING, consume_rest=False):
        self.name = name
        self.default = default
        self.consume_rest = consume_rest