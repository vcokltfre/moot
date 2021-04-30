from os import getenv

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {
        "request": request,
        "discord_oauth": getenv("OAUTH_URL"),
    })
