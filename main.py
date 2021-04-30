from os import getenv

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from src.routing import frontend_router


if not getenv("IN_DOCKER"):
    load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None, apoenapi_url=None)
app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(frontend_router)

@app.get("/ping")
async def ping() -> dict:
    """Get a static ping response showing the site is online."""

    return dict(status="ok")
