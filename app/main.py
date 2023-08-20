from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.infrastructure.routes.v1 import portfolio as port_v1 

app = FastAPI()

app.include_router(port_v1.router, prefix="/v1")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)