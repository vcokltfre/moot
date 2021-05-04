from typing import Optional
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    avatar_hash: Optional[str]
    bio: Optional[str]
    banned: bool
    flags: int


@dataclass
class Moot:
    id: int
    author_id: int
    content: str
    reference: Optional[int]
    hide: bool
    flags: int
