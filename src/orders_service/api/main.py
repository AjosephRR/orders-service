import logging
from collections.abc import Awaitable, Callable
from time import perf_counter

from fastapi import FastAPI, Request, Response

from orders_service.api.routers import auth, orders

logger = logging.getLogger("orders_service.api")
app = FastAPI(title="Orders Service")


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    logger.info(
        "%s %s -> %s in %.6fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(orders.router)
app.include_router(auth.router)
