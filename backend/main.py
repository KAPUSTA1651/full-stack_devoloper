from fastapi import FastAPI
from routers import notes

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)