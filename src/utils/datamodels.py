from os import getenv
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from fastapi.responses import RedirectResponse


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


@dataclass
class Session:
    token: str
    author_id: int
    expires: datetime


@dataclass
class AuthState:
    user: User = field(default=None)
    session: Session = field(default=None)

    def request_auth(self) -> RedirectResponse:
        return RedirectResponse(getenv("OAUTH_URL"))
