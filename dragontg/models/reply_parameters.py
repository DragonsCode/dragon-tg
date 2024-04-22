from dataclasses import dataclass
from dragontg.models.parent import Parent

@dataclass
class ReplyParameters(Parent):
    message_id: int
    chat_id: int