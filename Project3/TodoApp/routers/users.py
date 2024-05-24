from fastapi import APIRouter,Depends,HTTPException, status, Path
# import models
# from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from ..models import Users
from pydantic import BaseModel , Field
from ..database import SessionLocal
from .auth import get_current_user
# from routers import auth
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'],deprecated = 'auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class PhoneUpdate(BaseModel):
    phone_number: str 

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
async def cahnge_password(user: user_dependency,db:db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code = 401,detail="Not Authenticated")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code = 401,detail="Error on passowrd change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phone_number/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def cahnge_phone_number(user: user_dependency,db:db_dependency,phone_number:str):

    if user is None:
        raise HTTPException(status_code=401,detail = "Authenticationn Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    if user_model is None:
        raise HTTPException(status_code = 404,detail = "Todo Not Found.")
    
#     phone_number
    db.add(user_model)
    db.commit()