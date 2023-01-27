from fastapi import HTTPException
import time
from typing import Dict
from datetime import datetime

# import decouple 
import jwt 
from decouple import config
from jwt.exceptions import DecodeError, ExpiredSignatureError


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

print("testing ok")

def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if 'expires' in decoded_token:
            exp = decoded_token['expires']
            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise HTTPException(status_code=401, detail="Token expired")
            return decoded_token
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid JWT signature")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    
def verifyUrl(email: str):
    try:
        token = signJWT(email)
        new_Generate = token["access_token"]
        return "http://127.0.0.1:8000/user/verify?token=" + new_Generate.decode("utf-8");
    except:
        return {}
    
    
def resetLink(email: str):
    try:
        token = signJWT(email)
        new_Generate = token["access_token"]
        return "http://127.0.0.1:8000/user/reset?token=" + new_Generate.decode("utf-8");
    except:
        return {}