from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from decouple import config
from fastapi import Request
from jwt import ExpiredSignatureError

from ...models.models import User


class TokenHelper:
    __ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
    __REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
    __ALGORITHM = "HS512"
    __JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    __JWT_REFRESH_SECRET_KEY = config('JWT_REFRESH_SECRET_KEY')

    @classmethod
    def create_access_token(cls, user: User) -> Dict[str, str]:
        expires_delta = datetime.utcnow() + timedelta(minutes=cls.__ACCESS_TOKEN_EXPIRE_MINUTES)

        token_claims = {"user_id": user.id,
                        "user_email": user.email,
                        "username": user.username,
                        "expires": str(expires_delta)}
        encoded_jwt = jwt.encode(token_claims, cls.__JWT_SECRET_KEY, cls.__ALGORITHM)
        return {"access_token": "bearer " + encoded_jwt}

    @classmethod
    def decode_jwt(cls, request: Request) -> Optional[dict]:
        authorization_header_value: str = request.headers.get("Authorization")
        if not authorization_header_value:
            return None

        scheme, _, token = authorization_header_value.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return None

        try:
            decoded_jwt = jwt.decode(token, cls.__JWT_SECRET_KEY, [cls.__ALGORITHM])
        except ExpiredSignatureError as e:  # , JWTError
            return {"error": e}

        return decoded_jwt  # if decoded_jwt["expires"] >= datetime.utcnow() else None

    @classmethod
    def create_refresh_token(cls, user: User) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=cls.__REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"user_id": user.id,
                     "user_email": user.email,
                     "username": user.username,
                     "expires": expires_delta}
        encoded_jwt = jwt.encode(to_encode, cls.__JWT_REFRESH_SECRET_KEY, cls.__ALGORITHM)
        return encoded_jwt  # if decoded_jwt["expires"] >= datetime.utcnow() else None
