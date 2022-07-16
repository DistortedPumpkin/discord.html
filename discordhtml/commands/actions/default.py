from .core import Action
from ...utils import BREAK

class SendMessage(Action):
    CONTENT_REQUIRED = True
    
    async def execute(self, ctx):
        channel = int(self.data.get('channel', ctx.channel.id))
        await ctx.send(self.data['content'], to=channel)


class Condition(Action):
    CONTENT_REQUIRED = True

    async def execute(self, ctx):
        if not eval(self.data['content']):
            return BREAK


class Execute(Action):
    CONTENT_REQUIRED = True

    async def execute(self, ctx):
        exec(ctx)
