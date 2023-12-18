# In the name of GOD

import jwt
import base64
import random
import json
import uuid
from datetime import datetime, timedelta


class Encryption:

    def __init__(self, service_shared_key:str, code_keys:dict=None):
        self.service_shared_key = service_shared_key
        self.code_keys = code_keys or {}
