from fastapi import FastAPI
# import httpx

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Caching proxy is running"}

@app.api_route("/{path:path}", methods=["GET"])
async def proxy(path: str):
    print(f"Requested path: {path}")

    