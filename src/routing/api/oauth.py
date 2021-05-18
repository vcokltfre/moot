from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.utils.oauth import get_user_details


router = APIRouter()

@router.get("/callback")
async def auth_callback(request: Request) -> RedirectResponse:
    """Authenticate the user with Discord OAuth."""

    user = await get_user_details(request.state.session, request.query_params["code"])

    userid = int(user["id"])
    username = user["username"] + "#" + user["discriminator"]
    avatar = user.get("avatar", None)

    session = await request.state.db.user_login(userid, username, avatar)

    response = RedirectResponse("/")
    response.set_cookie("moot_session_token", session.token)
    return response
