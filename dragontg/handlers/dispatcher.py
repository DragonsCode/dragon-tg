from dragontg.models.parent import Parent
from dragontg.models.message import Message
from dragontg.models.user import User
from dataclasses import dataclass, field

@dataclass
class Dispatcher(Parent):
    message_handlers: list[tuple] = field(default_factory=list[tuple])

    def add_message_handler(self, handler: tuple):
        self.message_handlers.append(handler)
    
    def message_handler(self, filters: dict = {}):
        def wrapper(handler):
            try:
                self.add_message_handler((handler, filters))
            except Exception as e:
                print("IN dispatcher.py: message_handler error: ", e)
        return wrapper
    
    async def handle_message(self, update: dict, message: Message, bot: User):
        for h in self.message_handlers:
            if not h[1]:
                await h[0](update, message, bot)
                return
            else:
                dispatch = True
                for k, v in h[1].items():
                    if k in update and update[k] != v:
                        dispatch = False
                        return
                await h[0](update, message, bot)
                return