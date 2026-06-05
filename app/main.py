
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

from . import model
from .database import engine, get_db
from .schemas import TravelCreate, TravelResponse,UserCreate,UserResponse

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


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
def create_tour(post: TravelCreate):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        INSERT INTO tour (name, city, duration, cost)
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """,
        (post.name, post.city, post.duration, post.cost)
    )

    new_tour = cursor.fetchone()

    conn.commit()
    conn.close()

    return {"data": new_tour}


@app.get("/tour")
def get_tours():

    conn, cursor = get_psycopg_db()

    cursor.execute("SELECT * FROM tour")

    tours = cursor.fetchall()

    conn.close()

    return {"data": tours}


@app.get("/tour/{id}")
def get_tour(id: int):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        SELECT * FROM tour
        WHERE id = %s
        """,
        (id,)
    )

    tour = cursor.fetchone()

    conn.close()

    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    return {"data": tour}


@app.put("/tour/{id}")
def update_tour(id: int, post: TravelCreate):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        UPDATE tour
        SET name = %s,
            city = %s,
            duration = %s,
            cost = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.name, post.city, post.duration, post.cost, id)
    )

    updated_tour = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    return {"data": updated_tour}


@app.delete("/tour/{id}")
def delete_tour(id: int):

    conn, cursor = get_psycopg_db()

    cursor.execute(
        """
        DELETE FROM tour
        WHERE id = %s
        RETURNING *
        """,
        (id,)
    )

    deleted_tour = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    return {"message": "Tour deleted successfully"}


@app.post("/sqltour", response_model=TravelResponse)
def create_sql_tour(
    post: TravelCreate,
    db: Session = Depends(get_db)
):

    new_tour = model.Travel(
        name=post.name,
        city=post.city,
        duration=post.duration,
        cost=post.cost
    )

    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)

    return new_tour


@app.get("/sqltour")
def get_sql_tours(db: Session = Depends(get_db)):

    tours = db.query(model.Travel).all()

    return tours


@app.get("/sqltour/{id}")
def get_sql_tour(id: int, db: Session = Depends(get_db)):

    tour = db.query(model.Travel).filter(
        model.Travel.id == id
    ).first()

    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    return tour


@app.put("/sqltour/{id}")
def update_sql_tour(
    id: int,
    updated_data: TravelCreate,
    db: Session = Depends(get_db)
):

    tour_query = db.query(model.Travel).filter(
        model.Travel.id == id
    )

    tour = tour_query.first()

    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    tour_query.update(
        updated_data.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return tour_query.first()


@app.delete("/sqltour/{id}")
def delete_sql_tour(
    id: int,
    db: Session = Depends(get_db)
):

    tour_query = db.query(model.Travel).filter(
        model.Travel.id == id
    )

    tour = tour_query.first()

    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    tour_query.delete(synchronize_session=False)

    db.commit()

    return {"message": "Tour deleted successfully"}


@app.get("/")
def home():

    return {"message": "FastAPI is working"}


@app.post("/sqluser", response_model=UserResponse)
def create_sql_user(
    post: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = model.User(
        email=post.email,
        password=post.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user