from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import time


app = FastAPI(
    title="Continuous Performance Benchmarking Platform",
    description="API used for continuous performance testing and regression detection.",
    version="1.0.0"
)


class Item(BaseModel):
    name: str
    value: int = 1


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.get("/api/products/{product_id}")
def get_product(product_id: int):

    digest = hashlib.sha256(
        str(product_id).encode()
    ).hexdigest()

    return {
        "id": product_id,
        "sku": f"SKU-{product_id:06d}",
        "digest": digest
    }


@app.post("/api/items")
def create_item(item: Item):

    return {
        "id": item.value,
        "name": item.name,
        "status": "created"
    }


@app.get("/api/slow")
def slow_endpoint():

    time.sleep(0.05)

    return {
        "status": "ok",
        "delay_ms": 50
    }