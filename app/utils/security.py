import random
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from app.core import settings
from app.db import db_helper
from app.models import User


def generate_otp_code() -> str:
    return f"{random.randint(0, 9999):04}"


security = HTTPBearer()


class AuthManager:
    def __init__(self, secret_key: str, algorithm: str, token_validity: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_validity = token_validity


    def generate_token(self, user_id: int) -> str:
        expiration_date = datetime.now(timezone.utc) + timedelta(days=settings.TOKEN_VALIDITY)
        payload = {
            "sub": str(user_id),
            "exp": expiration_date
        }
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        return token


    async def student_auth(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> User:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            result = await session.execute(
                select(User).where(
                    User.id==int(user_id),
                    User.type=="student",
                    User.is_active==True
                )
            )

            student = result.scalar_one_or_none()

            if student is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")

            return student

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")


    async def admin_auth(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.get_scoped_session),
    ) -> User:
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            result = await session.execute(
                select(User).where(
                    User.id==int(user_id),
                    User.type=="admin",
                    User.is_active==True
                )
            )
            admin = result.scalar_one_or_none()

            if admin is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")

            return admin

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")


class PasswordManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


auth_manager = AuthManager(
    secret_key = settings.SECRET_KEY,
    algorithm = settings.ALGORITHM,
    token_validity = settings.TOKEN_VALIDITY
)


password_manager = PasswordManager()
