from fastapi import APIRouter, Request, Response

from src.utils.oauth import get_user_details


router = APIRouter()

@router.get("/callback")
async def auth_callback(request: Request) -> Response:
    """Authenticate the user with Discord OAuth."""

    user = await get_user_details(request.state.session, request.query_params["code"])

    print(user)
