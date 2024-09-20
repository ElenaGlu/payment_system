import os
import datetime
import base64
import hashlib
import jwt

from app.config import settings


def create_hash(password: str, salt=os.urandom(32)) -> str:
    """
    Password hashing.
    :param password: str
    :param salt: random bytes
    :return: Hash of the string
    """
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    storage = salt + key
    return base64.b64encode(storage).decode('ascii').strip()


def create_token_redis(id_user):
    """
    """
    payload = {"sub": "admin",
               "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
               }
    token = jwt.encode(payload, settings.KEY, algorithm="HS256")
    return f"{id_user}:{token}"
