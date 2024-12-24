from fastapi import FastAPI

from routers import auth, roast

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router, prefix="/auth")
app.include_router(roast.router, prefix="/roast")

