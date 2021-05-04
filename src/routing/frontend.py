from os import getenv

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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
    })
