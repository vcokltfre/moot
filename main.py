from os import getenv

from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from aiohttp import ClientSession
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from src.utils.ids import IDGenerator
from src.utils.database import Database
from src.routing import frontend_router, api_router


if not getenv("IN_DOCKER"):
    load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None, apoenapi_url=None)
app.mount("/static", StaticFiles(directory="static"), "static")
app.include_router(frontend_router)
app.include_router(api_router)

templates = Jinja2Templates(directory="templates")
session = ClientSession()
db = Database()
ids = IDGenerator()

@app.on_event("startup")
async def on_startup() -> None:
    """Connect the database on startup."""

    await db.ainit()

@app.middleware("http")
async def attach(request: Request, call_next) -> Response:
    """Attach the ClientSession, database and idgen to requests."""

    request.state.session = session
    request.state.db = db
    request.state.ids = ids

    return await call_next(request)

@app.middleware("http")
async def authorize(request: Request, call_next) -> Response:
    """Authorize the request."""

    session = request.cookies.get("moot_session_token", "")

    request.state.auth = await db.get_auth(session)

    return await call_next(request)

@app.exception_handler(HTTPException)
async def handler(request: Request, exc: HTTPException) -> Response:
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {
            "request": request,
        })
    return Response(exc.detail, exc.status_code)

@app.get("/ping")
async def ping() -> dict:
    """Get a static ping response showing the site is online."""

    return dict(status="ok")
