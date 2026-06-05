from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

from .. import model,utils
from ..database import engine, get_db
from ..schemas import TravelCreate, TravelResponse,UserCreate,UserResponse

router = APIRouter()

@router.post("/sqltour", response_model=TravelResponse)
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


@router.get("/sqltour")
def get_sql_tours(db: Session = Depends(get_db)):

    tours = db.query(model.Travel).all()

    return tours


@router.get("/sqltour/{id}")
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


@router.put("/sqltour/{id}")
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


@router.delete("/sqltour/{id}")
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


@router.get("/")
def home():

    return {"message": "FastAPI is working"}
