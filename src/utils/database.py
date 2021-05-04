from os import getenv
from typing import Optional

from asyncpg import create_pool, Pool

from .datamodels import User, Moot


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

        created_user = await self.pool.fetchrow("INSERT INTO Users (id, username, avatar_hash) VALUES ($1, $2, $3) RETURNING *;")

        return User(**dict(created_user))
