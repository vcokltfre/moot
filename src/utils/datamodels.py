from os import getenv
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from fastapi.responses import RedirectResponse
from pydantic import BaseModel, constr

from .bitfield import BitField
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

    @property
    def bits(self) -> BitField:
        return BitField(self.flags)

    @property
    def admin(self) -> bool:
        return bool(self.bits[0])

    @property
    def userbio(self) -> str:
        return self.bio or "This user has no bio."


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

    @property
    def _content(self) -> str:
        if self.hide:
            return "The content of this post has been hidden by the Moot moderation team."
        return self.content


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
    use_sample: bool = False

    @property
    def content(self) -> str:
        if self.use_sample:
            return "\n".join(self.moot._content[:1024].split("\n")[:20]) + ("..." if len(self.moot._content) > 1024 else "")
        return self.moot._content


class NewPost(BaseModel):
    content: constr(max_length=32000)
