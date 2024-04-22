from dataclasses import dataclass
from typing import List
from .parent import Parent

@dataclass
class Chat(Parent):
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    is_forum: bool = None
    active_usernames: List[str] = None