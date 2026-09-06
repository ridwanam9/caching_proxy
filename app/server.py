from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Caching proxy is running"}