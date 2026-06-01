from fastapi import FastAPI,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import model
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


class Travel(BaseModel):
    name: str
    city: str
    duration: int
    cost: int

def get_psycopg_db():
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
    conn, cursor = get_psycopg_db()

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


@app.post("/SQLtour")
def post_tour(post : Travel,db:Session = Depends(get_db)):
    new_tour = model.Travel(
        name = post.name,
        city = post.city,
        duration = post.duration,
        cost = post.cost
    )
    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)
    return {"Tour" : new_tour}



@app.get("/tour")
def get_tours():

    conn, cursor = get_psycopg_db()

    cursor.execute("SELECT * FROM tour")
    data = cursor.fetchall()

    conn.close()

    return {"data": data}


@app.get("/")
def home():
    return {"message": "FastAPI is working"}


@app.get("/tour/{id}")
def tour_by_id(id: int):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        SELECT * FROM tour WHERE id = %s
        """,
        (id,)
    )
    tour = cursor.fetchone()
    conn.close()

    return {"data": tour}


@app.delete("/tour/{id}")
def delete_by_id(id: int):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        DELETE FROM tour WHERE id = %s
        """,
        (id,)
    )

    conn.commit()

    conn.close()

    return {"message": f"Tour with id {id} deleted successfully"}


@app.put("/tour/{id}")
def update_by_id(id: int, post: Travel):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        UPDATE tour
        SET country = %s,
            city = %s,
            duration = %s,
            cost = %s
        WHERE id = %s
        """,
        (post.country, post.city, post.duration, post.cost, id)
    )

    conn.commit()
    conn.close()

    return {"message": "Tour updated successfully"}


@app.get("/coursealchemy")
def country(db: Session = Depends(get_db)):
    return {"message": "sqlalchemy orm working"}