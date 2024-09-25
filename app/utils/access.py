import os
import datetime
import base64
import hashlib
import jwt

from sqlalchemy import select
from app.database import async_session
from app.models import User, Wallet

from exceptions import AppError, ErrorType
from app.config import settings


class Access:
    @staticmethod
    async def login(email: str, password: str):
        async with async_session() as session:
            user = (await session.execute(
                select(User).where(User.email == email))).scalars().one_or_none()
            if user:
                password_hash = Access.create_hash(password)
                if user.hashed_password == '123':                   #change
                    return {
                        'id': user.id,
                        'email': user.email,
                        'full_name': user.full_name,
                    }
                    # data_token = Access.create_token_redis(user.id)
                    # connection_redis.setex(data_token, 2419200, '')
                    # return data_token.split(":")[2]
                else:
                    raise AppError(
                        {
                            'error_type': ErrorType.ACCESS_ERROR,
                            'description': 'Invalid email or password'
                        }
                    )
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'User is not registered.It is necessary to register'
                    }
                )

    @staticmethod
    async def account(user_id: int):
        async with async_session() as session:
            accounts = (await session.execute(
                select(Wallet).where(Wallet.user_id == user_id))).scalars().all()
            if accounts:
                tmp = []
                for account in accounts:
                    tmp_dict = {
                        'id': account.id,
                        'name wallet': account.name_wallet,
                        'balance': account.balance,
                    }
                    tmp.append(tmp_dict)
            return tmp

    @staticmethod
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

    @staticmethod
    def create_token_redis(id_user):
        """
        """
        payload = {"sub": "admin",
                   "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
                   }
        token = jwt.encode(payload, settings.KEY, algorithm="HS256")
        return f"{id_user}:{token}"
