from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl

app = FastAPI()

class travel(BaseModel):
    country: str
    city: str
    duration: str
    cost: str
    website: HttpUrl

@app.post("/germany")
def create_post(post : travel):
    return {"data" : post}

@app.get("/germany")
def get_travels():
    return travel

@app.get("/")
def get_api():
    return {"django" : "fastapi"}

@app.get("/hungary")
def hungary():
    return {"budapest" : "Pecs"}
