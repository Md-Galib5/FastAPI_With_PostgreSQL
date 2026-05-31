from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Travel(BaseModel):
    country: str
    city: str
    duration: int
    cost: int

def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="Tour",
        user="postgres",
        password="galibSQL",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    return conn, cursor

@app.post("/tour")
def create_tour(post: Travel):
    conn, cursor = get_db()

    cursor.execute(
        """
        INSERT INTO tour (country, city, duration, cost)
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """,
        (post.country, post.city, post.duration, post.cost)
    )
    new_data = cursor.fetchone()

    conn.commit()
    conn.close()

    return {"data": new_data}

@app.get("/tour")
def get_tours():

    conn, cursor = get_db()

    cursor.execute("SELECT * FROM tour")
    data = cursor.fetchall()

    conn.close()

    return {"data": data}

@app.get("/")
def home():
    return {"message": "FastAPI is working"}