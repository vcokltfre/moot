from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from src.utils.datamodels import ResolvedMoot, NewPost


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_index(request: Request) -> HTMLResponse:
    auth = request.state.auth

    if not auth.user:
        return auth.request_auth()

    user = auth.user

    moots = await request.state.db.get_all_recent_moots(15)
    users = await request.state.db.get_users(list(set([moot.author_id for moot in moots])))
    users = {user.id: user for user in users}

    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
        "moots": [ResolvedMoot(users[moot.author_id], moot) for moot in moots],
    })

@router.get("/users/{userid}")
async def get_userpage(userid: int, request: Request) -> HTMLResponse:
    auth = request.state.auth

    if not auth.user:
        return auth.request_auth()

    user = auth.user
    moots = await request.state.db.get_recent_moots(userid, 15)

    return templates.TemplateResponse("user.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
        "moots": [ResolvedMoot(user, moot) for moot in moots],
    })

@router.get("/moots/{id}")
async def get_userpage(id: int, request: Request) -> HTMLResponse:
    auth = request.state.auth

    if "discord" in request.headers.get("User-Agent", "").lower():
        moot = await request.state.db.get_moot(id)

        return templates.TemplateResponse("og.html", {
            "request": request,
            "desc": moot.content[:140] + "...",
        })

    if not auth.user:
        return auth.request_auth()

    moot = await request.state.db.get_moot(id)
    user = await request.state.db.get_user(moot.author_id)

    return templates.TemplateResponse("viewmoot.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
        "moot": ResolvedMoot(user, moot),
    })

@router.get("/new")
async def new(request: Request) -> HTMLResponse:
    auth = request.state.auth

    if not auth.user:
        return auth.request_auth()

    user = auth.user

    return templates.TemplateResponse("new.html", {
        "request": request,
        "username": user.username,
        "userid": user.id,
        "avatar_url": user.avatar_url,
    })

@router.post("/new/post")
async def new_post(data: NewPost, request: Request) -> dict:
    auth = request.state.auth

    if not auth.user:
        raise HTTPException(403, "Not authorized.")

    user = auth.user

    if len(data.content) < 280:
        raise HTTPException(400, "Bad content. Content too short!")

    id = request.state.ids.next()

    await request.state.db.create_moot(id, user.id, data.content)

    return {
        "id": id,
    }
