from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException, Depends
from typing_extensions import Annotated
from modals.users import Users
from fastapi.security import  OAuth2PasswordBearer
from starlette import status

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
  
    payload = {'sub': username, 'id': user_id, 'role': role , 'exp' : datetime.utcnow() + expires_delta}
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/users/token')

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        expires = payload.get('exp')
        
        if username is None or user_id is None or expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')

        if datetime.utcnow() > (datetime.utcfromtimestamp(expires)):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Session expired.')
            
        return {'username': username, 'id': user_id, 'user_role': user_role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')

user_dependency = Annotated[dict, Depends(get_current_user)]
