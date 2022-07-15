from typing import Dict, Optional, Any, Type
from .errors import MissingData
from .parser import Parser
from .commands import Command, Context
from .commands.actions import Action
from discord import Intents, Game, Client
from .commands.actions.default import SendMessage


class Bot:
    def __init__(self):
        self.storage: Dict[str, Any] = {"bot": self}
        self.commands: Dict[str, Command] = {}
        self.action_classes: Dict[str, Type[Action]] = {}
        self.parser = Parser(self)
        self.dpy: Optional[Client] = None  # Will be set on .run() once the user already set the prefix & token
        self.prefix: Optional[str] = None  # Will be set on .run() once the user set the prefix

        for cls in (SendMessage, ):
            self.add_action_class(cls)
    
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(self.prefix):
            cmd_name, *args = message.content[len(self.prefix):].split()
            cmd = self.commands.get(cmd_name)
            if cmd:
                context = Context(message, cmd, self, args)
                await cmd.invoke(context)
    
    def run(self):
        if not self.storage.get('token'):
            raise MissingData('token')
        if not self.storage.get('prefix'):
            raise MissingData('prefix')
        
        self.prefix = self.storage['prefix']
        
        intents_value = self.storage.get('intents_value')
        if intents_value:
            intents = Intents()
            intents.value = intents_value
        else:
            intents = Intents(messages=True, guilds=True, message_content=True)
        
        
        self.dpy = Client(
            max_messages=None, intents=intents, 
            owner_id=self.storage.get('owner_id'), owner_ids=self.storage.get('owner_ids'),
            activity=Game(self.storage['activity']) if self.storage.get('activity') else None
        )
        self.dpy.on_message = self.on_message

        self.dpy.run(self.storage['token'])
    
    def add_command(self, command):
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command
    
    def add_action_class(self, class_: type):
        if not issubclass(class_, Action):
            raise TypeError("Action class must derive from commands.actions.Action")
        self.action_classes[class_.__name__.lower()] = class_
    
    def load_file(self, filename, is_main_file: bool = False):
        with open(filename) as file:
            content = file.read()
        self.parser.parse(content, is_main_file)
