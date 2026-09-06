import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

origin = None


@app.api_route("/{path:path}", methods=["GET"])
async def proxy(path: str):
    target_url = f"{origin}/{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code
    )