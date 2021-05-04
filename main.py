from os import getenv

from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from aiohttp import ClientSession
from fastapi.staticfiles import StaticFiles

from src.routing import frontend_router, api_router
from src.utils.database import Database


if not getenv("IN_DOCKER"):
    load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None, apoenapi_url=None)
app.mount("/static", StaticFiles(directory="static"), "static")
app.include_router(frontend_router)
app.include_router(api_router)

session = ClientSession()
db = Database()

@app.on_event("startup")
async def on_startup() -> None:
    """Connect the database on startup."""

    await db.ainit()

@app.middleware("http")
async def attach(request: Request, call_next) -> Response:
    """Attach the ClientSession and database to requests."""

    request.state.session = session
    request.state.db = db

    return await call_next(request)

@app.middleware("http")
async def authorize(request: Request, call_next) -> Response:
    """Authorize the request."""

    session = request.cookies.get("moot_session_token", "")

    request.state.auth = await db.get_auth(session)

    return await call_next(request)

@app.get("/ping")
async def ping() -> dict:
    """Get a static ping response showing the site is online."""

    return dict(status="ok")
