from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import database, model, utils, schemas,oauth2

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
    access_token = oauth2.create_access_token(
        data = {"user_id" : user.id},
        expires_delta=timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token,"token_type" : "barer"}