import httpx
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

load_dotenv()

app = FastAPI(
    title="E-Commerce API Gateway"
)


SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL"),
    "products": os.getenv("PRODUCT_SERVICE_URL"),
    "orders": os.getenv("ORDER_SERVICE_URL")
}
if not all(SERVICES.values()):
    raise RuntimeError("Service URLs are not configured")

async def forward_request(
    request: Request,
    service_url: str,
    path: str
):
    body = await request.body()

    headers = dict(request.headers)

    headers.pop("host", None)

    async with httpx.AsyncClient() as client:

        response = await client.request(
            method=request.method,
            url=f"{service_url}/{path}",
            headers=headers,
            content=body,
            params=request.query_params
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers={
            "content-type": response.headers.get(
                "content-type",
                "application/json"
            )
        }
    )


@app.get("/")
def home():
    return {
        "message": "API Gateway is running"
    }


@app.api_route(
    "/auth/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def auth_gateway(
    path: str,
    request: Request
):
    return await forward_request(
        request,
        SERVICES["auth"],
        f"auth/{path}"
    )


@app.api_route(
    "/products/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def products_gateway(
    path: str,
    request: Request
):
    return await forward_request(
        request,
        SERVICES["products"],
        f"products/{path}"
    )


@app.api_route(
    "/orders/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def orders_gateway(
    path: str,
    request: Request
):
    return await forward_request(
        request,
        SERVICES["orders"],
        f"orders/{path}"
    )