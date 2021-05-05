from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.utils.ids import get_datetime


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_index(request: Request) -> HTMLResponse:
    auth = request.state.auth

    if not auth.user:
        return auth.request_auth()

    user = auth.user

    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
    })

@router.get("/users/{userid}")
async def get_userpage(userid: int, request: Request) -> HTMLResponse:
    auth = request.state.auth

    if not auth.user:
        return auth.request_auth()

    user = auth.user

    moots = await request.state.db.get_recent_moots(userid, 15)

    for moot in moots:
        moot.date = get_datetime(moot.id).strftime("%Y-%m-%d at %H:%M:%S")
        moot.username = user.username
        moot.avatar_url = user.avatar_url
        moot.userid = user.id

    return templates.TemplateResponse("user.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
        "moots": [moot for moot in moots],
    })
