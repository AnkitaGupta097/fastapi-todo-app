from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import db_dependency
from dtos.users_dto import UserDTO 
from dtos.change_password_dto import ChangePasswordDTO
from modals.users import Users
from passlib.context import CryptContext
from starlette import status
from typing_extensions import Annotated
from helper import create_access_token, user_dependency
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])

bcrypt_context = CryptContext(schemes="bcrypt", deprecated='auto')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserDTO):
   
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
   user = db.query(Users).filter(Users.username == form_data.username and bcrypt_context.verify(form_data.password, Users.hashed_password)).first()
   if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')
   
   token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))     
   return {'access_token': token, 'token_type': 'bearer'}


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: ChangePasswordDTO):

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password) or bcrypt_context.verify(user_verification.new_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()