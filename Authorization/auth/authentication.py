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

    @staticmethod
    def create_access_token(user_data, jti=None):
        token = jwt_tools.create_jwt(user_data, settings.ACCESS_TOKEN_EXP , jti)
        jwt_tools.store_in_cash(token)
        return token

    @staticmethod
    def create_refresh_token(user_data, jti=None):
        token = jwt_tools.create_jwt( user_data, settings.REFRESH_TOKEN_EXP, jti)
        jwt_tools.store_in_cash(token)
        return token

    @staticmethod
    def delete_old_user_tokens(username):
        jwt_tools.delete_old_user_tokens(username)

    @staticmethod
    def delete_old_user_login_tokens(username):
        jwt_tools.delete_old_user_login_tokens(username)


class EmailAuthentication:
    @classmethod
    def create_and_store_otp(cls, email, prefix_key=""):
        otp = random.randint(1000,9999)
        key = prefix_key + email
        databases['redis_db'].setex(name=key, value=otp, time=550)
        return otp

    @classmethod
    def verify_otp(cls, email, otp, prefix_key=""):
        key = prefix_key + email
        stored_otp = databases['redis_db'].get(key)
        print("otp: ", stored_otp)
        return stored_otp and int(stored_otp) == int(otp)