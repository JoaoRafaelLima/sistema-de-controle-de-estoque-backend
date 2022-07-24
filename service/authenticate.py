from functools import wraps
from flask import request
import jwt
import os

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if request.headers.get("authorization"):
            token = request.headers["authorization"]
            try:
                dec = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
                return f(dec, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"Error": "Sessão expirada"}
            except jwt.InvalidSignatureError:
                return {"Error": "Token invalido"}
            except jwt.DecodeError:
                return {"Error": "Token invalido"}
        else:
            return {"Error": "sem permissao"}
        
         
    return wrapper