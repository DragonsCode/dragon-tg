from dataclasses import dataclass
from dragontg.models.parent import Parent
from .user import User
from .message import Message

from ..handlers.dispatcher import Dispatcher

from ..methods.parent import Request, Response
from ..methods.get_me import get_me
from ..methods.send_message import send_message

class Bot(Parent):
    token: str
    dispatcher: Dispatcher
    offset: int = 0
    timeout: int = 60

    async def get_me(self) -> User:
        res = await get_me(self.token)
        if res[0]:
            return User.from_kwargs(**res[1])
        else:
            print(f"Error {res[1][0]}: {res[1][1]}")
    
    async def get_updates(self, offset: int, timeout: int) -> list[dict]:
        dt = dict(offset=offset, timeout=timeout)
        try:
            response = await Request('/getUpdates', self.token, data=dt).post_response()
            j = response.result
        except ValueError:  # incomplete data
            return
        if not response.ok or not j:
            return
        return j
    
    async def send_message(self, chat_id: int, text: str, reply_to_message_id: int = None):
        res = await send_message(self.token, chat_id, text, reply_to_message_id)
        if not res:
            return
        res['from_user'] = res['from']
        del res['from']
        return Message.from_kwargs(**res)

    async def long_polling(self, skip_updates: bool = False) -> None:
        bot = await self.get_me()
        print(f"Starting long polling for @{bot.username}...")
        if skip_updates:
            print("Skipping updates...")
            res = await self.get_updates(self.offset, self.timeout)
            if not res:
                print("No updates to skip!")
            else:
                self.offset = res[-1]['update_id'] + 1
                print(f"Skipping updates until {self.offset}...")
                print(f"{len(res)} updates skipped, {self.offset} left!")
        while True:
            j = await self.get_updates(self.offset, self.timeout)
            if not j:
                continue
            for r in j:
                from_user = r['message']['from']
                r['message']['from_user'] = from_user
                del r['message']['from']
                m = Message.from_kwargs(**r['message'])
                if m.text:
                    await self.dispatcher.handle_message(r, m, bot)
                self.offset = r['update_id'] + 1