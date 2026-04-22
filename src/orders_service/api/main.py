from fastapi import FastAPI
from orders_service.api.routers import orders

app = FastAPI(title="Orders Service")

app.include_router(orders.router)
