import discord
from typing import Union

class _BreakSentinel:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return '...'


def to_bool(value: Union[str, bool]):
    if isinstance(value, bool):
        return value
    
    if value.lower() in ('true', 't', '1', 'on'):
        return True
    return False


BREAK = _BreakSentinel()
MISSING = discord.utils.MISSING