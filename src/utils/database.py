from os import getenv
from typing import Optional
from datetime import datetime

from asyncpg import create_pool, Pool

from .datamodels import User, Session


class Database:
    """A database class to aid making requests."""

    def __init__(self) -> None:
        self.pool: Pool = None

    async def ainit(self) -> None:
        """Asynchronously initialize the database."""

        self.pool = await create_pool(getenv("DB_DSN"))

    async def get_user(self, id: int) -> Optional[User]:
        """Get a user from the database.

        Args:
            id (int): The user's Discord ID from OAuth.

        Returns:
            Optional[User]: The user object.
        """

        raw_user = await self.pool.fetchrow("SELECT * FROM Users WHERE id = $1;", id)

        if not raw_user:
            return None

        return User(**dict(raw_user))

    async def create_user(self, id: int, username: str, avatar: str = None) -> User:
        """Create a new Moot user.

        Args:
            id (int): The user's Discord ID from OAuth.
            username (str): The user's initial username.
            avatar (str): The user's avatar from Discord, if available. Defaults to None.

        Returns:
            User: The user object created.
        """

        created_user = await self.pool.fetchrow("INSERT INTO Users (id, username, avatar_hash) VALUES ($1, $2, $3) RETURNING *;", id, username, avatar)

        return User(**dict(created_user))

    async def get_session(self, token: str) -> Optional[Session]:
        """Get a user's existing session.

        Args:
            token (str): The session token to find the session by.

        Returns:
            Optional[Session]: The user's session.
        """

        raw_session = await self.pool.fetchrow("SELECT * FROM UserSessions WHERE token = $1;", token)

        if not raw_session:
            return None

        session = Session(**dict(raw_session))

        if session.expires < datetime.utcnow():
            await self.pool.execute("DELETE FROM UserSessions WHERE token = $1;", token)
            return None

        return session

    async def create_session(self, token: str, user: int, expires: datetime) -> Session:
        """Create a new session for a user.

        Args:
            token (str): The session token to use.
            user (int): The user ID whose session will be created.
            expires (datetime): The expiry time of the session.

        Returns:
            Session: The session object created.
        """

        created_session = await self.pool.fetchrow("INSERT INTO UserSessions (token, author_id, exppires) VALUES ($1, $2, $3) RETURNING *;", token, user, expires)

        return User(**dict(created_session))
