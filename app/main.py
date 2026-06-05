from fastapi import FastAPI, Depends, HTTPException, status
from .routers import user,tour,auth

app = FastAPI()

app.include_router(tour.router)
app.include_router(user.router)
app.include_router(auth.router)
