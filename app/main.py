from fastapi import FastAPI, Depends, HTTPException, status
from .routers import user,tour,auth
from . import model
from .database import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tour.router)
app.include_router(user.router)
app.include_router(auth.router)
