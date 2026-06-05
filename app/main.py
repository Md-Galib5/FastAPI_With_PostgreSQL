from fastapi import FastAPI, Depends, HTTPException, status
from .routers import user,tour

app = FastAPI()

app.include_router(tour.router)
app.include_router(user.router)

