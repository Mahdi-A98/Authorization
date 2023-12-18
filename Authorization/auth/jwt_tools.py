def decode_jwt_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return None, HTTPException(detail='Invalid signature', status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.ExpiredSignatureError:
        return None, HTTPException(detail='Token has expired', status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return None, HTTPException(detail='Parse Error', status_code=status.HTTP_401_UNAUTHORIZED)
    return payload , None # Return payload and error if accures 

def verify_jti(payload:dict):
    jti = payload.get('jti')
    if not databases['redis_db'].get(jti):
        raise HTTPException(detail='Token not found', status_code=status.HTTP_401_UNAUTHORIZED)
    if user_identifier:= databases['redis_db'].get(jti):
        user_identifier = user_identifier.decode() if isinstance(user_identifier, bytes) else user_identifier
        return user_identifier
    return None
