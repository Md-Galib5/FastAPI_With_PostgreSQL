from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from .. import oauth2
from .. import model
from ..database import get_db
from ..schemas import TravelCreate, TravelResponse

router = APIRouter(
    prefix="/tour",
    tags=["Tour"]
)


@router.post("/", response_model=TravelResponse)
def create_sql_tour(
    post: TravelCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
):

    new_tour = model.Travel(
        name=post.name,
        city=post.city,
        duration=post.duration,
        cost=post.cost,
        creator_id=current_user.id
    )

    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)

    return new_tour


@router.get("/", response_model=list[TravelResponse])
def get_sql_tours(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
):

    tours = db.query(model.Travel).filter(
        model.Travel.creator_id == current_user.id
    ).all()

    return tours


@router.get("/{id}", response_model=TravelResponse)
def get_sql_tour(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
):

    tour = db.query(model.Travel).filter(
        model.Travel.id == id
    ).first()

    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )

    # authorization check
    if tour.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this tour"
        )

    return tour


@router.put("/{id}", response_model=TravelResponse)
def update_sql_tour(
    id: int,
    updated_data: TravelCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
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

    # authorization check
    if tour.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this tour"
        )

    tour_query.update(
        updated_data.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return tour_query.first()


@router.delete("/{id}")
def delete_sql_tour(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
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

    # authorization check
    if tour.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this tour"
        )

    tour_query.delete(synchronize_session=False)

    db.commit()

    return {"message": "Tour deleted successfully"}