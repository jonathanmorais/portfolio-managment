from fastapi import FastAPI

from app.routes.v1 import portfolio as port_v1 

app = FastAPI()

app.include_router(port_v1.router, prefix="/v1")
