from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import database, model, utils, schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(database.get_db)
):

    user = db.query(model.User).filter(
        model.User.email == user_credentials.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    if not utils.verify_password(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    return {"token": "Successfully Login"}