import httpx

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()

origin = None

cache = {}


@app.api_route("/{path:path}", methods=["GET"])
async def proxy(path: str, request: Request):

    cache_key = str(request.url.path)

    if request.url.query:
        cache_key += f"?{request.url.query}"

    print("Cache key:", cache_key)

    if cache_key in cache:
        print("CACHE HIT")

        cached_response = cache[cache_key]

        return JSONResponse(
            content=cached_response["body"],
            status_code=cached_response["status_code"],
            headers={
                "X-Cache": "HIT"
            }
        )

    print("CACHE MISS")

    target_url = f"{origin}/{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            target_url,
            params=request.query_params
        )

    cache[cache_key] = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.json()
    }

    print(cache[cache_key])

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
        headers={"X-Cache": "MISS"}
    )