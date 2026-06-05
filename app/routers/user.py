from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

from .. import model,utils
from ..database import engine, get_db
from ..schemas import TravelCreate, TravelResponse,UserCreate,UserResponse

router = APIRouter()

@router.post("/sqluser", response_model=UserResponse)
def create_sql_user(
    post: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = utils.hash_password(post.password)
    post.password = hashed_password


    new_user = model.User(
        email=post.email,
        password=post.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user