from abc import ABC, abstractmethod

class Action(ABC):
    CONTENT_REQUIRED = False
    
    def __init__(self, data=None):
        self.data = data or {}
    
    @abstractmethod
    async def execute(self, context):
        raise NotImplementedError