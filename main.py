from fastapi import FastAPI
from api.v1.endpoints import calculation

app = FastAPI()

app.include_router(calculation.router, prefix="/api/v1", tags=["Calculation"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
