from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime , timedelta
from flask import jsonify

def expire_date(days: int): 
    now = datetime.now()
    return now + timedelta(days)    

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2) },
                   key=getenv("SECRET"), algorithm='HS256')
    return token.encode('utf-8')

def validate_token(token, output = False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=['HS256'])
        decode(token, key=getenv("SECRET"), algorithms=['HS256'])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Expired token"})
        response.status_code = 401
        return response