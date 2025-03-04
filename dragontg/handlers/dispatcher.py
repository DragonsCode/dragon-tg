import logging
from dataclasses import dataclass, field
from dragontg.models.parent import Parent
from dragontg.models.message import Message
from dragontg.models.user import User

# Logging setup
# logging.basicConfig(
#     format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
#     level=logging.DEBUG
# )

@dataclass
class Dispatcher(Parent):
    message_handlers: list[tuple] = field(default_factory=list[tuple])

    def add_message_handler(self, handler: tuple):
        self.message_handlers.append(handler)
        logging.debug(f'Handler {handler[0].__name__} added with filters {handler[1]}')
    
    def message_handler(self, filters: dict = {}):
        def wrapper(handler):
            try:
                self.add_message_handler((handler, filters))
            except Exception as e:
                logging.error(f'Error in message_handler: {e}', exc_info=True)
        return wrapper
    
    def get_nested_value(self, d, keys):
        """Retrieve a nested value from a dictionary using a list of keys."""
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return None
        return d
    
    async def handle_message(self, update: dict, message: Message, bot: User = None):
        for h in self.message_handlers:
            if not h[1]:  # No filters, execute handler
                await h[0](update, message)
                logging.info(f'Update {update["update_id"]} handled by {h[0].__name__} without filters')
                return
            else:
                dispatch = True
                logging.debug(f'Checking filters {h[1]} for update {update["update_id"]}')
                for k, v in h[1].items():
                    keys = k.split('.')  # Split key for nested access
                    value = self.get_nested_value(update['message'], keys)
                    if value != v:  # Filter fails if value doesn't match
                        dispatch = False
                        break
                if dispatch:
                    await h[0](update, message)
                    logging.info(f'Update {update["update_id"]} handled by {h[0].__name__}')
                    return
        logging.warning(f'Update {update["update_id"]} not handled by any handler')
