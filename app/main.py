from fastapi import FastAPI
from .routers import olhcvs

app = FastAPI(dependencies=[])

app.include_router(olhcvs.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
