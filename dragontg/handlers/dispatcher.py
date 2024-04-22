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
                print(f"Update {update['update_id']} is handled!")
                return
            else:
                dispatch = True
                print(h[1].items())
                # print(update)
                for k, v in h[1].items():
                    print(k, v)
                    if '.' in k:
                        inner_k = k.split('.')
                        print(inner_k)
                        if inner_k[0] in update['message']:
                            if update['message'][inner_k[0]][inner_k[1]] != v:
                                dispatch = False
                                break
                    if k in update['message'] and update['message'][k] != v:
                        print(f"Update {update['update_id']} is not handled, because {k} != {v}!")
                        dispatch = False
                        break
                if dispatch:
                    await h[0](update, message, bot)
                    print(f"Update {update['update_id']} is handled!")
                    return
        print(f"Update {update['update_id']} is not handled!")