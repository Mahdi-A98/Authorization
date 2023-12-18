from pydantic_settings import BaseSettings, SettingsConfigDict
import logging.config
from typing import Dict, Any

class Settings(BaseSettings):
    SECRET_KEY : str

    REDIS_HOST : str
    REDIS_PORT : str
    REDIS_DATABASE : str
    REDIS_PASSWORD : str = ""

    AUTH_ACC_KEY1 : str
    AUTH_ACC_KEY2 : str
    AUTH_ACC_KEY3 : str

    AUTH_NTF_KEY1 : str
    AUTH_NTF_KEY2 : str
    AUTH_NTF_KEY3 : str

    AUTH_POD_KEY1 : str
    POD_AUTH_SHARED_KEY : str

    ACCESS_TOKEN_EXP : int
    REFRESH_TOKEN_EXP : int
    TOKEN_PREFIX : str

    ACCOUNT_AUTH_SHARED_KEY : str
    NTF_AUTH_SHARED_KEY: str

    ACCOUNT_SERVICE_URL : str
    NOTIFICATION_SERVICE_URL :str

    CELERY_BROKER_URL: str 
    CELERY_RESULT_BACKEND : str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")
