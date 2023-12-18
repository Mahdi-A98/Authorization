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

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s %(asctime)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s %(asctime)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
# LOGGING_CONFIG = {
#     "version": 1,
#     "handlers": {
#         "default": {
#             "class": "logging.StreamHandler",
#             "formatter": "http",
#             "stream": "ext://sys.stderr"
#         }
#     },
#     "formatters": {
#         "http": {
#             "format": "%(levelname)s [%(asctime)s] %(name)s - %(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         }
#     },
#     'loggers': {
#         'httpx': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#         },
#         'httpcore': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#         },
#     }
# }

# logging.config.dictConfig(LOGGING_CONFIG)