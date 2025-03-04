from dragontg.models.chat import Chat
from dragontg.models.user import User
from dragontg.models.parent import Parent

from dragontg.methods.send_message import send_message

from dataclasses import dataclass, field

@dataclass
class Message(Parent):
    message_id: int
    date: int
    text: str
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
    
    @chat.setter
    def from_user(self, val):
        self._from_user = User.from_kwargs(**val)
    
    async def reply(self, token: str, text: str):
        result = await send_message(token, self.chat.id, text, self.message_id)
        return result

    def __repr__(self):
        return f"Message(message_id={self.message_id}, date={self.date}, text={self.text}, from_user={self.from_user}, chat={self.chat})"
    
    def __str__(self):
        return f"Message(message_id={self.message_id}, date={self.date}, text={self.text}, from_user={self.from_user}, chat={self.chat})"