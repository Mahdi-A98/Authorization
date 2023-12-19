# In the name of GOD


from config import settings

from fastapi.exceptions import HTTPException
from fastapi import status

from datetime import datetime, timedelta
from . import jwt_tools
from db.db import databases
import random



class JWTAuthentication:
    @classmethod
    def authenticate(cls, access_token=None, refresh_token=None):
        if refresh_token:
            return cls.authenticat_with_token(refresh_token)
        if access_token:
            return cls.authenticat_with_token(access_token)
        raise HTTPException(detail="Token should be provided", status_code=status.HTTP_401_UNAUTHORIZED)
        


    @staticmethod
    def authenticat_with_token(jwt_token:str):

        if not jwt_token.startswith(settings.TOKEN_PREFIX + " "):       # TODO creatin jwt config in settings
            raise HTTPException(detail="Token prefix doesn't match", status_code=status.HTTP_401_UNAUTHORIZED)
        
        prefix, jwt_token = jwt_token.split()  # clean the token

        payload, error = jwt_tools.decode_jwt_token(jwt_token)
        if payload is None:
            raise error
        user_identifier = payload.get('user_identifier')
        if user_identifier is None:
            raise HTTPException(detail='User identifier not found in JWT', status_code=status.HTTP_401_UNAUTHORIZED)

        if not jwt_tools.verify_exp(payload): 
            raise HTTPException(detail="Token expired", status_code=status.HTTP_401_UNAUTHORIZED)
        
        if not user_identifier.split("@sep@")[0] == jwt_tools.verify_jti(payload).split("@sep@")[0]:
            raise HTTPException(detail="Invalid user", status_code=status.HTTP_401_UNAUTHORIZED)
        
        username, email = user_identifier.split("@sep@")
        return username, email
