from fastapi import FastAPI
from .routers import olhcvs, economic_indicators

app = FastAPI(dependencies=[])

app.include_router(olhcvs.router)
app.include_router(economic_indicators.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
