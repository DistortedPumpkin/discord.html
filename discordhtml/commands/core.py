from typing import List
from .actions.core import Action
from .params import Parameter
from ..errors import MissingRequiredArgument
from ..utils import BREAK
from discord.http import handle_message_parameters
import discord

MISSING = discord.utils.MISSING


class Context:
    def __init__(self, message, command: "Command", bot, args: List[str] = None):
        self.message = message 
        self.command = command
        self.bot = bot
        self.args = args or []
        self.storage = {"ctx": self}
        self._parse_arguments()

    
    def _parse_arguments(self) -> dict:
        for i, param in enumerate(self.command.params):
            if len(self.args) > i:
                if i + 1 == len(self.command.params):  # This is the last Parameter
<<<<<<< HEAD
                    self.storage[param.name] = ' '.join(self.args[i if not param.consume_rest else i:])
=======
                    storage[param.name] = ' '.join(self.args[i if not param.consume_rest else i:])
>>>>>>> 976729a96b96861a1f34c48e5d6a0da7251086de
                else:
                    self.storage[param.name] = self.args[i]
            else:
                if param.default is MISSING:
                    raise MissingRequiredArgument(param.name)
                else:
                    self.storage[param.name] = param.default
                
    
    async def send(self, content: str, to=None, parse_args=True):
        to = to or self.channel
        if isinstance(to, (discord.TextChannel, discord.DMChannel, discord.GroupChannel)):
            to = to.id
        if (embed := self.bot.parser.parse_for_embed(content, self)):
            content = None
        content = self.bot.parser.parse_content_with_variables(content, self) if content and parse_args else content
        with handle_message_parameters(content=content, embed=embed) as params:
            await self.bot.dpy.http.send_message(to, params=params)
        
    @property
    def author(self):
        return self.message.author
    
    @property
    def channel(self):
        return self.message.channel
    
    @property
    def guild(self):
        return self.message.guild

    def to_dict(self):
        return {
            "content": self.message.content,
            "author": self.author,
            "channel": self.channel.id,
            "guild" : self.guild.id,
        }


class Command:
    def __init__(self, name: str, *, aliases: List[str] = None, params: List[Parameter] = None, actions: List[Action] = None):
        self.name = name
        self.aliases = aliases or []
        self.params = params or []
        self.actions = actions or []
    
    async def invoke(self, ctx: Context):
        for action in self.actions:
            if await action.execute(ctx) == BREAK:
                break
    
    def add_action(self, action: Action):
        self.actions.append(action)