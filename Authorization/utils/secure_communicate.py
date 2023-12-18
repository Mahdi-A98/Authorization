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
    @staticmethod
    def Encode(key:str, message:str):
        assert isinstance(message, str), "message should be string  "           
        enc=[]
        for i in range(len(message)):
                key_c = key[i % len(key)]
                enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
        return base64.urlsafe_b64encode("".join(enc).encode(errors="ignore")).decode(errors="ignore") 
    
    @staticmethod
    def Decode(key, message): 
        dec = []              
        message = base64.urlsafe_b64decode(message).decode(errors="ignore")
        for i in range(len(message)):     
                key_c = key[i % len(key)] 
                dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256)) 
        return "".join(dec)