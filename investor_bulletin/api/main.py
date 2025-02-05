from uvicorn import run
from fastapi import FastAPI

from api.routes import init_routes

app = init_routes(FastAPI())

if __name__ == "__main__":
    run("api.main:app")
