# IN the name of GOD
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field, EmailStr, StringConstraints
from pydantic.types import SecretStr

from typing_extensions import Annotated


class UserLogin(BaseModel):
    username : Optional[str] = None
    email: Optional[EmailStr] = Field(unique=True)
    password : SecretStr


class UserRegister(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    username : Annotated[str, StringConstraints(to_lower=True)]
    email: Optional[EmailStr] = Field(unique=True)
    password : SecretStr

class UserUpdate(UserRegister):
    is_active : Optional[bool] = True
    is_superuser : Optional[bool] = False
    is_deleted : Optional[bool] = False
    image : Optional[str] = None

class AuthorizationTokens(BaseModel):
    access_token : Optional[str] = None
    refresh_token : Optional[str] = None