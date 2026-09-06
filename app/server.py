import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

origin = None

cache = {}


@app.api_route("/{path:path}", methods=["GET"])
async def proxy(path: str):
    cache_key = path

    if cache_key in cache:
        print("CACHE HIT")

        cached_response = cache[cache_key]

        return JSONResponse(
            content=cached_response,
            headers={"X-Cache": "HIT"}
        )

    print("CACHE MISS")

    target_url = f"{origin}/{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    cache[cache_key] = response.json()

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
        headers={"X-Cache": "MISS"}
    )