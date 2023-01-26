import time
from typing import Dict
from app.model import AccountSchema

# import decouple 
import jwt 
from decouple import config


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
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
    
    
def verifyUrl(email: str):
    try:
        token = signJWT(email)
        new_Generate = token["access_token"]
        return "http://127.0.0.1:8000/user/verify?token=" + new_Generate.decode("utf-8");
    except:
        return {}