import httpx
from fastapi import FastAPI

app = FastAPI()

origin = None


@app.api_route("/{path:path}", methods=["GET"])
async def proxy(path: str):
    target_url = f"{origin}/{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    return response.json()