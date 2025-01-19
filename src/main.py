from fastapi import FastAPI

from routers import auth, roast

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(roast.router, prefix="/roast")

