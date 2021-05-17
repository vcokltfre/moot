from os import getenv
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from .ids import get_datetime


@dataclass
class User:
    id: int
    username: str
    avatar_hash: Optional[str]
    bio: Optional[str]
    banned: bool
    flags: int

    @property
    def avatar_url(self) -> str:
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}"


@dataclass
class Moot:
    id: int
    author_id: int
    content: str
    reference: Optional[int]
    hide: bool
    flags: int

    @property
    def human_time(self) -> str:
        return get_datetime(self.id).strftime("%Y-%m-%d at %H:%M:%S")


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


@dataclass
class ResolvedMoot:
    user: User
    moot: Moot


class NewPost(BaseModel):
    content: str
