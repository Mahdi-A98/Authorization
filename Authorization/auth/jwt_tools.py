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

def verify_exp(payload:dict):
    exp = payload.get('exp')
    return exp > datetime.now().timestamp()




def store_in_cash(jwt_token):
    payload, error = decode_jwt_token(jwt_token)
    if payload:
        jti = payload['jti']
        user_identifier = payload['user_identifier']
        timeout = int(payload['exp'] - payload['iat'])
        databases['redis_db'].setex(name=jti, value=user_identifier, time=timeout)
    else:
        raise error

def create_jwt(user_data, expiration_hours, jti=None):
    payload = {
        'user_identifier': user_data.get('username') + "@sep@" + user_data.get("email"),
        'exp': int((datetime.now() + timedelta(hours=expiration_hours)).timestamp()),
        'iat': datetime.now().timestamp(),
        'jti': user_data.get("username") + '@login@' + (jti or uuid.uuid4().hex),
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token

def delete_jti_from_cache(jtis:list):
    if len(jtis) < 1:
        return "No jti to delete"
    result = databases['redis_db'].delete(*jtis)
    return result


def delete_old_user_tokens(username):
    user_tokens_jtis = databases['redis_db'].keys(username + "*")
    delete_jti_from_cache(user_tokens_jtis)

def delete_old_user_login_tokens(username):
    user_tokens_jtis = databases['redis_db'].keys(username + "@login@" +"*")
    delete_jti_from_cache(user_tokens_jtis)