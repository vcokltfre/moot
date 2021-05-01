from os import getenv

from aiohttp import ClientSession
from fastapi.exceptions import HTTPException


def build_oauth_token_request(code: str) -> tuple:
    """Given a code, return a dict of query params needed to complete the oath flow."""
    query = dict(
        client_id=int(getenv("CLIENT_ID")),
        client_secret=getenv("CLIENT_SECRET"),
        grant_type="authorization_code",
        code=code,
        redirect_uri=f"{getenv('BASE_URL')}/api/callback",
        scope="identify",
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return query, headers

async def get_user_details(session: ClientSession, code: str) -> dict:
    try:
        token_params, token_headers = build_oauth_token_request(code)
        token = await (await session.post("https://discord.com/api/oauth2/token", data=token_params, headers=token_headers)).json()
        auth_header = {"Authorization": f"Bearer {token['access_token']}"}
        user = await (await session.get("https://discord.com/api/users/@me", headers=auth_header)).json()
    except KeyError as e:
        raise HTTPException(401, "Unknown error while creating token")

    return user
