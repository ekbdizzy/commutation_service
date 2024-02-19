from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
async def healthcheck():
    return {"status": "ok"}

