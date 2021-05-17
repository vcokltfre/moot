from os import getenv
from secrets import token_hex
from typing import Optional, List
from datetime import datetime, timedelta

from asyncpg import create_pool, Pool

from .datamodels import User, Session, AuthState, Moot


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

        created_session = await self.pool.fetchrow("INSERT INTO UserSessions (token, author_id, expires) VALUES ($1, $2, $3) RETURNING *;", token, user, expires)

        return Session(**dict(created_session))

    async def user_login(self, user_id: int, username: str, avatar: str) -> Session:
        """Execute the full user login process.

        Args:
            user_id (int): The user ID to log in.
            username (str): The user's username.
            avatar (str): The user's avatar.

        Returns:
            Session: The user's logged in session.
        """

        expires = datetime.utcnow() + timedelta(days=14)

        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id, username, avatar)

        return await self.create_session(token_hex(64), user.id, expires)

    async def get_auth(self, token: str) -> AuthState:
        """Get a user's authentication state.

        Args:
            token (str): The user's session token.

        Returns:
            AuthState: The user's authentication state.
        """

        session = await self.get_session(token)
        if not session:
            return AuthState()

        user = await self.get_user(session.author_id)

        return AuthState(user, session)

    async def get_moot(self, id: int) -> Optional[Moot]:
        """Get a specific Moot by ID.

        Args:
            id (int): The ID to fetch the Moot for.

        Returns:
            Optional[Moot]: The Moot object.
        """

        raw_moot = await self.pool.fetchrow("SELECT * FROM Moots WHERE id = $1;", id)

        if not raw_moot:
            return None

        return Moot(**dict(raw_moot))

    async def get_recent_moots(self, userid: int, number: int, offset: int = 0) -> List[Moot]:
        """Get the most recent moots from a user.

        Args:
            userid (int): The user's ID to query Moots from.
            number (int): The max number of Moots to return.
            offset (int): The offset to fetch Moots at. Defaults to 0.

        Returns:
            List[Moot]: The list of Moots.
        """

        moots = await self.pool.fetch("SELECT * FROM Moots WHERE author_id = $1 ORDER BY id DESC LIMIT $2 OFFSET $3;", userid, number, offset)

        return [Moot(**dict(raw_moot)) for raw_moot in moots]

    async def get_all_recent_moots(self, number: int, offset: int = 0) -> List[Moot]:
        """Get the most recent moots.

        Args:
            number (int): The max number of Moots to return.
            offset (int): The offset to fetch Moots at. Defaults to 0.

        Returns:
            List[Moot]: The list of Moots.
        """

        moots = await self.pool.fetch("SELECT * FROM Moots ORDER BY id DESC LIMIT $1 OFFSET $2;", number, offset)

        return [Moot(**dict(raw_moot)) for raw_moot in moots]

    async def get_users(self, ids: List[int]) -> List[User]:
        """Get a user from the database.

        Args:
            ids (List[int]): The user IDs to look up.

        Returns:
            List[User]: The user objects.
        """

        raw_users = await self.pool.fetch("SELECT * FROM Users WHERE id = any($1::bigint[]);", tuple(ids))

        return [User(**dict(raw_user)) for raw_user in raw_users]

    async def create_moot(self, id: int, author_id: int, content: str) -> Moot:
        """Create a new Moot.

        Args:
            id (int): The ID of the Moot to create.
            author_id (int): The author of the Moot's ID.
            content (str): The content of the moot.

        Returns:
            Moot: The created Moot object.
        """

        created_moot = await self.pool.fetchrow("INSERT INTO Moots (id, author_id, content) VALUES ($1, $2, $3) RETURNING *;", id, author_id, content)

        return Moot(**dict(created_moot))
