from fastapi import FastAPI


app = FastAPI(docs_url=None, redoc_url=None, apoenapi_url=None)

@app.get("/ping")
async def ping() -> dict:
    """Get a static ping response showing the site is online."""

    return dict(status="ok")
