from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Learning FastAPI")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
