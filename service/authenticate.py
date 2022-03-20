from functools import wraps
from flask import request
import jwt

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if request.headers.get("authorization"):
            token = request.headers["authorization"]
        if not token:
            return {"Error": "sem permissao"}
        else:
            try:
                dec = jwt.decode(token, "teste", algorithms=["HS256"])
                return f(dec, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"Error": "Sessão expirada"}
            except jwt.InvalidSignatureError as e:
                return {"Error": "Token invalido"}
         
    return wrapper