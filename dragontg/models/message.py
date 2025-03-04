from typing import TYPE_CHECKING
from dragontg.models.chat import Chat
from dragontg.models.user import User
from dragontg.models.parent import Parent
# from dragontg.models.bot import Bot

from dragontg.methods.send_message import send_message

from dataclasses import dataclass

if TYPE_CHECKING:
    from dragontg.models.bot import Bot  # Only for type checkers

@dataclass
class Message(Parent):
    message_id: int
    date: int
    text: str
    bot: 'Bot' = None
    _from_user: User = None
    _chat: Chat = None

    @property
    def chat(self):
        return self._chat
    
    @chat.setter
    def chat(self, val):
        self._chat = Chat.from_kwargs(**val)
    
    @property
    def from_user(self):
        return self._from_user
    
    @from_user.setter
    def from_user(self, val):
        self._from_user = User.from_kwargs(**val)
    
    async def reply(self, text: str):
        if not self.bot:
            raise ValueError("Bot instance not set in Message")
        result = await send_message(self.bot.token, self.chat.id, text, self.message_id)
        return result

    def __repr__(self):
        return f"Message(message_id={self.message_id}, date={self.date}, text={self.text}, bot={self.bot}, from_user={self.from_user}, chat={self.chat})"
    
    def __str__(self):
        return f"Message(message_id={self.message_id}, date={self.date}, text={self.text}, bot={self.bot}, from_user={self.from_user}, chat={self.chat})"