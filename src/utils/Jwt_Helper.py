import jwt
from datetime import datetime, timedelta, timezone
from ..config import Config

def createToken(username:str, email:str):
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=7)

    payload = {
        "username" : username,
        "email" : email,
        "exp" : expires_at
    }

    token = jwt.encode(payload=payload,key=Config.SECRET)
    return token