import httpx

from fastapi import FastAPI, Request, Response


app = FastAPI(
    title="E-Commerce API Gateway"
)


SERVICES = {
    "auth": "http://127.0.0.1:8001",
    "products": "http://127.0.0.1:8002",
    "orders": "http://127.0.0.1:8003"
}


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