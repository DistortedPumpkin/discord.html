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
        self.storage = self.parse_arguments()

    
    def parse_arguments(self) -> dict:
        storage = {}
        for i, param in enumerate(self.command.params):
            if len(self.args) > i:
                if i + 1 == len(self.command.params):  # This is the last Parameter
                    storage[param.name] = self.args[i if not param.consume_rest else i:]
                else:
                    storage[param.name] = self.args[i]
            else:
                if param.default is MISSING:
                    raise MissingRequiredArgument(param.name)
                else:
                    storage[param.name] = param.default
        return storage
                
    
    async def send(self, content: str, to=None, parse_args=True):
        to = to or self.channel
        if isinstance(to, (discord.TextChannel, discord.DMChannel, discord.GroupChannel)):
            to = to.id
        content = self.bot.parser.parse_content_with_variables(content, self) if parse_args else content
        with handle_message_parameters(content=content) as params:
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