from __future__ import annotations

import json
import logging
import os
import time
import uuid
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field

logger = logging.getLogger("rheinshield.workload")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI(
    title="RheinCommerce Synthetic Order API",
    version="1.0.0",
    description="Synthetic portfolio workload. No customer data.",
    docs_url=None if os.getenv("RHEINSHIELD_MODE") == "lab-live" else "/docs",
)

_requests: dict[str, deque[float]] = defaultdict(deque)
_orders: dict[str, dict[str, object]] = {}
RATE_LIMIT = 60


class OrderRequest(BaseModel):
    product_id: str = Field(pattern=r"^prd-[a-z0-9]{4,12}$")
    quantity: int = Field(ge=1, le=20)


class OrderResponse(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    status: str
    synthetic: bool = True


def _log(event: str, **fields: object) -> None:
    logger.info(json.dumps({"timestamp": datetime.now(UTC).isoformat(), "event": event, **fields}, sort_keys=True))


@app.middleware("http")
async def security_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
    client_key = request.client.host if request.client else "unknown"
    now = time.monotonic()
    bucket = _requests[client_key]
    while bucket and bucket[0] < now - 60:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT:
        _log("rate_limit", correlation_id=correlation_id, client="synthetic-client")
        return Response(status_code=429, headers={"Retry-After": "60", "X-Correlation-ID": correlation_id})
    bucket.append(now)
    started = time.perf_counter()
    response = await call_next(request)
    response.headers.update({
        "X-Correlation-ID": correlation_id,
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
        "Cache-Control": "no-store",
    })
    _log("http_request", correlation_id=correlation_id, method=request.method, path=request.url.path, status=response.status_code, duration_ms=round((time.perf_counter() - started) * 1000, 2))
    return response


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "healthy", "synthetic": True, "service": "rheincommerce-order-api"}


@app.get("/ready")
def ready() -> dict[str, object]:
    return {
        "status": "ready",
        "dependencies": {"configuration": "ok", "structured_logging": "ok"},
        "key_vault_mode": "configuration-contract-only" if os.getenv("KEY_VAULT_URI") else "local-fixture",
    }


@app.get("/products")
def products() -> list[dict[str, object]]:
    return [
        {"product_id": "prd-secure01", "name": "Synthetic Security Token", "stock": 42},
        {"product_id": "prd-cloud02", "name": "Synthetic Cloud Voucher", "stock": 18},
    ]


@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderRequest) -> OrderResponse:
    order_id = f"ord-{uuid.uuid4().hex[:12]}"
    record = OrderResponse(order_id=order_id, product_id=order.product_id, quantity=order.quantity, status="accepted")
    _orders[order_id] = record.model_dump()
    _log("synthetic_order_created", order_id=order_id, product_id=order.product_id, quantity=order.quantity, data_classification="Synthetic")
    return record


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str) -> OrderResponse:
    if not order_id.startswith("ord-") or order_id not in _orders:
        raise HTTPException(status_code=404, detail="Synthetic order not found")
    return OrderResponse.model_validate(_orders[order_id])
